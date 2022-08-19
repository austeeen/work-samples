import json
import concurrent
import copy

from .utils.helpers import check_boto3, set_fleet_path, warn_user
from .utils.file_manager import FileManager
from .harvester import Harvester
from .S3 import S3Storage
from .robot_http import RobotHttp

class KeyFilter:
    @staticmethod
    def upload_needed(s3, key, copy_dest_bucket):
        if s3.resource_exists(key['bucket'], key['key']) or \
            (copy_dest_bucket and \
                s3.resource_exists(copy_dest_bucket, key['key'])):
            return False
        return True

    @staticmethod
    def put_key(cmd, key):
        if not KeyFilter.upload_needed(cmd.s3, key, cmd.args.copy_dest_bucket):
            # Upload already exists
            cmd.download_list.append(key)
        else:
            # We only need to upload/move
            cmd.upload_list.append(key)

    @staticmethod
    def filter(cmd):
        def exists_done(future):
            if future.exception():
                print ("Caught exeception {}".format(future.exception()))
            elif not future.result():
                cmd.download_list.append(future.key)
            else:
                cmd.upload_list.append(future.key)

        with concurrent.futures.ThreadPoolExecutor(32) as executor:
            for k in cmd.keys:
                if k['key'] and k['bucket']:
                    future = executor.submit(KeyFilter.upload_needed,
                                             cmd.s3, k, cmd.args.copy_dest_bucket)
                    future.key = k
                    future.add_done_callback(exists_done)

class HarvestCommand:
    def __init__(self, tool_args, excessive_key_count=500):
        self.args = tool_args
        self.no_prompt = self.args.force_yes
        self.excessive_key_count = excessive_key_count
        self.fleet_path = ""
        self.harvester = None
        self.s3 = None
        self.file_manager = None
        self.key_filter = KeyFilter()
        self.keys = []
        self.upload_list = []
        self.download_list = []
        self.saved_files = []

    def set_up(self):
        self.configure_fleet()
        self.configure_schedule()
        self.validate_context()
        self.generate_modules()

    def configure_fleet(self):
        PRIVATE

    def configure_schedule(self):
        if not self.args.schedule and not self.args.from_file:
            commands = RobotHttp(PRIVATE).list_commands()
            for command in commands:
                if command['command_type'] == 'PRIVATE' \
                        and command['status'] == 'issued':
                    print('[WARNING] There is an incomplete PRIVATE command on the robot.')
                    msg = ""
                    if self.args.throttle > 5:
                        self.args.throttle = 5
                        msg += "--throttle=5"
                    if msg:
                        print(f'[WARNING] Tuned args to {msg}')
                    break

    @staticmethod
    def validate_context():
        check_boto3(required=True)

    def generate_modules(self):
        self.harvester = Harvester(PRIVATE)
        self.s3 = S3Storage()
        self.file_manager = FileManager(self.args.out_dir)

    def harvest_image_keys(self, filter_object):
        self.keys = self.harvester.harvest_images(filter_object=filter_object, PRIVATE)

    def harvest_insight_data(self):
        self.keys = self.harvester.harvest_insight_data(
            file_list=self.args.file_list,
            filter_object=self.args.filter_object,
            PRIVATE
            num_threads=self.args.download_threads,
            from_file=self.args.from_file)

    def pull_data(self):
        if not len(self.keys):
            print("[WARNING] No keys were harvested.")
            return
        if self.args.force_upload:
            for k in self.keys:
                if k['key'] and k['bucket']:
                    self.upload_list.append(k)
        else:
            print(f"filtering {len(self.keys)} keys...")
            self.key_filter.filter(self)
        print(f"{len(self.upload_list)} upload keys and {len(self.download_list)} download keys.")
        self.upload_keys()
        if self.args.schedule:
            self.save_scheduled_keys()
            return
        self.copy_keys()
        self.download_keys()

    def upload_keys(self):
        if not len(self.upload_list):
            print("[WARNING] No keys to upload.")
            return

        if len(self.upload_list) > self.excessive_key_count:
            warn_user(f"upload list contains {len(self.upload_list)} keys, this may be excessive.",
                      self.no_prompt)

        results = self.harvester.upload_insight_images(PRIVATE)

        # MJP: Not sure if this is needed.
        #  Reliability is a huge problem when dealing with full res images.
        #  Leslie's theory is that images that 'fail' to upload actually are uploading.
        #  So unless there is an explicit failure, attempt to download anyways
        if not results and self.args.download_timeout > 0:
            return

        if type(results) == str:
            # upload_insight_images function returns a string message if the command was scheduled.
            self.download_list.extend(self.upload_list)
            print(results)
            return

        failed_keys = []
        for entry in results:
            result = json.loads(entry)
            failed_keys.extend(key for key in result['failed_keys'])

        self.download_list.extend([k for k in self.upload_list if k['key'] not in failed_keys])
        print(f"{len(self.download_list)} keys uploaded, {len(failed_keys)} failed to upload.")

    def save_scheduled_keys(self):
        if not len(self.download_list):
            print("[WARNING] No keys to schedule.")
            return

        self.file_manager.save_json(self.download_list, "scheduled_keys.json")

    @staticmethod
    def _copy_done(future):
        k = future.key
        if future.exception():
            print(f'Exception when copying {k}: {future.exception()}')
        elif future.result(): # Copied?
            print(f'Copied {k} to {future.copy_dest_bucket}')
        else:
            k = copy.deepcopy(k)
            k['bucket'] = future.copy_dest_bucket
            print(f'Using existing {k}')

    @staticmethod
    def _remove_done(future):
        k = future.key
        if future.exception():
            print(f'Exception when removing {k}: {future.exception()}')
        else:
            print(f'Removed {k}')

    @staticmethod
    def _copy_if_needed(s3, key, copy_dest_bucket):
        if not s3.resource_exists(copy_dest_bucket, key['key']):
            s3.copy_resource(key['bucket'], key['key'],
                             copy_dest_bucket, key['key'])
            return True
        return False

    def copy_keys(self):
        if not self.args.copy_dest_bucket:
            return # We are not copying anything

        if not len(self.download_list):
            print("[WARNING] No keys to copy.")
            return

        def copy_done(future):
            k = future.key
            if future.exception():
                print(f'Exception when copying {k}: {future.exception()}')
            else:
                print(f'Copied {k}')

        with concurrent.futures.ThreadPoolExecutor(self.args.download_threads) as executor:
            for k in self.download_list:
                future = executor.submit(HarvestCommand._copy_if_needed,
                                         self.s3, k, self.args.copy_dest_bucket)
                future.key = k
                future.copy_dest_bucket = self.args.copy_dest_bucket
                future.add_done_callback(HarvestCommand._copy_done)

    def download_keys(self):
        if not len(self.download_list):
            print("[WARNING] No keys to download.")
            return

        # If no-download was given clear the download list.
        # Go through the rest of the motions so that remove-s3 can be done.
        dl_list = self.download_list if not self.args.no_download else []

        if len(dl_list) > self.excessive_key_count:
            warn_user(f"download list contains {len(dl_list)} keys, this may be "
                      f"excessive.", self.no_prompt)

        if dl_list:
            print("Fetching and downloading keys from s3.")
            
        def file_downloaded(future):
            if future.exception():
                print ('Exception occurred during download of {}: {}'.format(
                       future.key['key'], future.exception()))
                return
            file_data = future.result()
            if not file_data:
                return
            file_path = self.file_manager.save_data(
                file_data=file_data,
                file_path=future.key['key'],
                pre_pend=future.key['vp_id'])
            if file_path:
                self.saved_files.append(file_path)

        get_resource_args = {}
        if self.args.download_timeout == 0:
            get_resource_args['sleep'] = 0 # Don't sleep for 5 seconds if no timeout
        with concurrent.futures.ThreadPoolExecutor(self.args.download_threads) as executor:
            for key in dl_list:
                future = executor.submit(self.s3.get_resource,
                                         bucket=key['bucket'],
                                         key=key['key'],
                                         timeout=self.args.download_timeout,
                                         **get_resource_args)
                future.key = key
                future.add_done_callback(file_downloaded)

        if dl_list:
            print(f"Harvested {len(self.saved_files)} files.")

        if self.args.remove_s3:
            print(f"Removing {len(self.upload_list)} objects from S3")

            self.s3.add_client() # For more efficient deletes
            with concurrent.futures.ThreadPoolExecutor(self.args.download_threads) as executor:
                for k in self.upload_list:
                    future = executor.submit(self.s3.remove_resource, k['bucket'], k['key'])
                    future.key = k
                    future.add_done_callback(HarvestCommand._remove_done)
