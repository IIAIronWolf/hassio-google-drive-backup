import json
from enum import Enum, unique
from os.path import abspath, join

from .boolvalidator import BoolValidator
from .floatvalidator import FloatValidator
from .intvalidator import IntValidator
from .regexvalidator import RegexValidator
from .stringvalidator import StringValidator
from .listvalidator import ListValidator
from .durationassecondsvalidator import DurationAsSecondsValidator
from ..logger import getLogger

logger = getLogger(__name__)


@unique
class Setting(Enum):
    # Basic snapshot settings
    MAX_SNAPSHOTS_IN_HASSIO = "max_snapshots_in_hassio"
    MAX_SNAPSHOTS_IN_GOOGLE_DRIVE = "max_snapshots_in_google_drive"
    DAYS_BETWEEN_SNAPSHOTS = "days_between_snapshots"
    SNAPSHOT_NAME = "snapshot_name"
    SNAPSHOT_TIME_OF_DAY = "snapshot_time_of_day"
    SNAPSHOT_PASSWORD = "snapshot_password"
    SPECIFY_SNAPSHOT_FOLDER = "specify_snapshot_folder"
    WARN_FOR_LOW_SPACE = "warn_for_low_space"
    LOW_SPACE_THRESHOLD = "low_space_threshold"

    # generational settings
    GENERATIONAL_DAYS = "generational_days"
    GENERATIONAL_WEEKS = "generational_weeks"
    GENERATIONAL_MONTHS = "generational_months"
    GENERATIONAL_YEARS = "generational_years"
    GENERATIONAL_DAY_OF_WEEK = "generational_day_of_week"
    GENERATIONAL_DAY_OF_MONTH = "generational_day_of_month"
    GENERATIONAL_DAY_OF_YEAR = "generational_day_of_year"
    GENERATIONAL_DELETE_EARLY = "generational_delete_early"

    # Partial snapshots
    EXCLUDE_FOLDERS = "exclude_folders"
    EXCLUDE_ADDONS = "exclude_addons"

    # UI Server Options
    USE_SSL = "use_ssl"
    CERTFILE = "certfile"
    KEYFILE = "keyfile"
    INGRESS_PORT = "ingress_port"
    PORT = "port"
    REQUIRE_LOGIN = "require_login"
    EXPOSE_EXTRA_SERVER = "expose_extra_server"

    # Add-on options
    VERBOSE = "verbose"
    NOTIFY_FOR_STALE_SNAPSHOTS = "notify_for_stale_snapshots"
    ENABLE_SNAPSHOT_STALE_SENSOR = "enable_snapshot_stale_sensor"
    ENABLE_SNAPSHOT_STATE_SENSOR = "enable_snapshot_state_sensor"
    SEND_ERROR_REPORTS = "send_error_reports"
    CONFIRM_MULTIPLE_DELETES = "confirm_multiple_deletes"
    ENABLE_DRIVE_UPLOAD = "enable_drive_upload"

    # Theme Settings
    BACKGROUND_COLOR = "background_color"
    ACCENT_COLOR = "accent_color"

    # Network and dns stuff
    DRIVE_EXPERIMENTAL = "drive_experimental"
    DRIVE_IPV4 = "drive_ipv4"
    IGNORE_IPV6_ADDRESSES = "ignore_ipv6_addresses"
    GOOGLE_DRIVE_TIMEOUT_SECONDS = "google_drive_timeout_seconds"
    GOOGLE_DRIVE_PAGE_SIZE = "google_drive_page_size"
    ALTERNATE_DNS_SERVERS = "alternate_dns_servers"
    DEFAULT_DRIVE_CLIENT_ID = "default_drive_client_id"
    DEFAULT_DRIVE_CLIENT_SECRET = "default_drive_client_secret"
    DRIVE_PICKER_API_KEY = "drive_picker_api_key"

    # Files and folders
    FOLDER_FILE_PATH = "folder_file_path"
    CREDENTIALS_FILE_PATH = "credentials_file_path"
    RETAINED_FILE_PATH = "retained_file_path"
    SECRETS_FILE_PATH = "secrets_file_path"
    BACKUP_DIRECTORY_PATH = "backup_directory_path"
    INGRESS_TOKEN_FILE_PATH = "ingress_token_file_path"
    CONFIG_FILE_PATH = "config_file_path"
    ID_FILE_PATH = "id_file_path"

    # endpoints
    HASSIO_URL = "hassio_url"
    DRIVE_URL = "drive_url"
    HOME_ASSISTANT_URL = "home_assistant_url"
    HASSIO_TOKEN = "hassio_header"
    AUTHENTICATE_URL = "authenticate_url"
    REFRESH_URL = "refresh_url"
    CHOOSE_FOLDER_URL = "choose_folder_url"
    ERROR_REPORT_URL = "error_report_url"
    DRIVE_HOST_NAME = "drive_host_name"
    DRIVE_REFRESH_URL = "drive_refresh_url"
    DRIVE_AUTHORIZE_URL = "drive_authorize_url"
    DRIVE_TOKEN_URL = "drive_token_url"

    # Timing and timeouts
    MAX_SYNC_INTERVAL_SECONDS = "max_sync_interval_seconds"
    SNAPSHOT_STALE_SECONDS = "snapshot_stale_seconds"
    PENDING_SNAPSHOT_TIMEOUT_SECONDS = "pending_snapshot_timeout_seconds"
    FAILED_SNAPSHOT_TIMEOUT_SECONDS = "failed_snapshot_timeout_seconds"
    NEW_SNAPSHOT_TIMEOUT_SECONDS = "new_snapshot_timeout_seconds"
    DOWNLOAD_TIMEOUT_SECONDS = "download_timeout_seconds"
    DEFAULT_CHUNK_SIZE = "default_chunk_size"
    DEBUGGER_PORT = "debugger_port"
    SERVER_PROJECT_ID = "server_project_id"
    LOG_LEVEL = "log_level"
    CONSOLE_LOG_LEVEL = "console_log_level"

    def default(self):
        return _DEFAULTS[self]

    def validator(self):
        return _VALIDATORS[self]

    def key(self):
        return self.value


_DEFAULTS = {
    # Basic snapshot settings
    Setting.MAX_SNAPSHOTS_IN_HASSIO: 4,
    Setting.MAX_SNAPSHOTS_IN_GOOGLE_DRIVE: 4,
    Setting.DAYS_BETWEEN_SNAPSHOTS: 3,
    Setting.SNAPSHOT_TIME_OF_DAY: "",
    Setting.SNAPSHOT_NAME: "{type} Snapshot {year}-{month}-{day} {hr24}:{min}:{sec}",
    Setting.SNAPSHOT_PASSWORD: "",
    Setting.SPECIFY_SNAPSHOT_FOLDER: False,
    Setting.WARN_FOR_LOW_SPACE: True,
    Setting.LOW_SPACE_THRESHOLD: 1024 * 1024 * 1024,

    # Generational backup settings
    Setting.GENERATIONAL_DAYS: 0,
    Setting.GENERATIONAL_WEEKS: 0,
    Setting.GENERATIONAL_MONTHS: 0,
    Setting.GENERATIONAL_YEARS: 0,
    Setting.GENERATIONAL_DAY_OF_WEEK: "mon",
    Setting.GENERATIONAL_DAY_OF_MONTH: 1,
    Setting.GENERATIONAL_DAY_OF_YEAR: 1,
    Setting.GENERATIONAL_DELETE_EARLY: False,

    # Partial snapshot settings
    Setting.EXCLUDE_FOLDERS: "",
    Setting.EXCLUDE_ADDONS: "",

    # UI Server settings
    Setting.USE_SSL: False,
    Setting.REQUIRE_LOGIN: False,
    Setting.EXPOSE_EXTRA_SERVER: False,
    Setting.CERTFILE: "/ssl/fullchain.pem",
    Setting.KEYFILE: "/ssl/privkey.pem",
    Setting.INGRESS_PORT: 8099,
    Setting.PORT: 1627,

    # Add-on options
    Setting.NOTIFY_FOR_STALE_SNAPSHOTS: True,
    Setting.ENABLE_SNAPSHOT_STALE_SENSOR: True,
    Setting.ENABLE_SNAPSHOT_STATE_SENSOR: True,
    Setting.SEND_ERROR_REPORTS: False,
    Setting.VERBOSE: False,
    Setting.CONFIRM_MULTIPLE_DELETES: True,
    Setting.ENABLE_DRIVE_UPLOAD: True,

    # Theme Settings
    Setting.BACKGROUND_COLOR: "#ffffff",
    Setting.ACCENT_COLOR: "#03a9f4",

    # Network and DNS settings
    Setting.ALTERNATE_DNS_SERVERS: "8.8.8.8,8.8.4.4",
    Setting.DRIVE_EXPERIMENTAL: False,
    Setting.DRIVE_IPV4: "",
    Setting.IGNORE_IPV6_ADDRESSES: False,
    Setting.GOOGLE_DRIVE_TIMEOUT_SECONDS: 180,
    Setting.GOOGLE_DRIVE_PAGE_SIZE: 100,

    # Remote endpoints
    Setting.HASSIO_URL: "http://hassio/",
    Setting.HASSIO_TOKEN: "",
    Setting.HOME_ASSISTANT_URL: "http://hassio/homeassistant/api/",
    Setting.DRIVE_URL: "https://www.googleapis.com",
    Setting.REFRESH_URL: "https://habackup.io/drive/refresh",
    Setting.AUTHENTICATE_URL: "https://habackup.io/drive/authorize",
    Setting.DRIVE_REFRESH_URL: "https://www.googleapis.com/oauth2/v4/token",
    Setting.DRIVE_AUTHORIZE_URL: "https://accounts.google.com/o/oauth2/v2/auth",
    Setting.DRIVE_TOKEN_URL: "https://oauth2.googleapis.com/token",
    Setting.CHOOSE_FOLDER_URL: "https://habackup.io/drive/picker",
    Setting.ERROR_REPORT_URL: "https://habackup.io/logerror",
    Setting.DRIVE_HOST_NAME: "www.googleapis.com",

    # File locations used to store things
    Setting.FOLDER_FILE_PATH: "/data/folder.dat",
    Setting.CREDENTIALS_FILE_PATH: "/data/credentials.dat",
    Setting.BACKUP_DIRECTORY_PATH: "/backup",
    Setting.RETAINED_FILE_PATH: "/data/retained.json",
    Setting.SECRETS_FILE_PATH: "/config/secrets.yaml",
    Setting.INGRESS_TOKEN_FILE_PATH: "/data/ingress.dat",
    Setting.CONFIG_FILE_PATH: "/data/options.json",
    Setting.ID_FILE_PATH: "/data/id.json",

    # Various timeouts and intervals
    Setting.SNAPSHOT_STALE_SECONDS: 60 * 60 * 3,
    Setting.PENDING_SNAPSHOT_TIMEOUT_SECONDS: 60 * 60 * 5,
    Setting.FAILED_SNAPSHOT_TIMEOUT_SECONDS: 60 * 15,
    Setting.NEW_SNAPSHOT_TIMEOUT_SECONDS: 5,
    Setting.MAX_SYNC_INTERVAL_SECONDS: 60 * 60,
    Setting.DEFAULT_DRIVE_CLIENT_ID: "933944288016-n35gnn2juc76ub7u5326ls0iaq9dgjgu.apps.googleusercontent.com",
    Setting.DEFAULT_DRIVE_CLIENT_SECRET: "",
    Setting.DRIVE_PICKER_API_KEY: "",
    Setting.DEFAULT_CHUNK_SIZE: 1024 * 1024 * 5,
    Setting.DOWNLOAD_TIMEOUT_SECONDS: 60,
    Setting.DEBUGGER_PORT: None,
    Setting.SERVER_PROJECT_ID: "",
    Setting.LOG_LEVEL: 'DEBUG',
    Setting.CONSOLE_LOG_LEVEL: 'INFO'
}

PRIVATE = [
    Setting.SNAPSHOT_PASSWORD,
    Setting.SNAPSHOT_NAME
]

_LOOKUP = {}
_VALIDATORS = {}


def getValidator(name, schema):
    if schema.endswith("?"):
        schema = schema[:-1]
    if schema.startswith("int("):
        # its a int
        parts = schema[4:-1]
        minimum = None
        maximum = None
        if parts.endswith(","):
            minimum = int(parts[0:-1])
        elif parts.startswith(","):
            maximum = int(parts[1:])
        else:
            digits = parts.split(",")
            minimum = int(digits[0])
            maximum = int(digits[1])
        return IntValidator(name, minimum, maximum)
    elif schema.startswith("float("):
        # its a float
        parts = schema[6:-1]
        minimum = None
        maximum = None
        if parts.endswith(","):
            minimum = float(parts[0:-1])
        elif parts.startswith(","):
            maximum = float(parts[1:])
        else:
            digits = parts.split(",")
            minimum = float(digits[0])
            maximum = float(digits[1])
        return FloatValidator(name, minimum, maximum)
    elif schema.startswith("bool"):
        # its a bool
        return BoolValidator(name)
    elif schema.startswith("str") or schema.startswith("url"):
        # its a url (treat it just like any string)
        return StringValidator(name)
    elif schema.startswith("match("):
        return RegexValidator(name, schema[6:-1])
    elif schema.startswith("list("):
        return ListValidator(name, schema[5:-1].split("|"))
    else:
        raise Exception("Invalid schema: " + schema)


# initalize validators
for setting in Setting:
    _LOOKUP[setting.value] = setting

with open(abspath(join(__file__, "..", "..", "..", "config.json"))) as f:
    addon_config = json.load(f)
for key in addon_config["schema"]:
    _VALIDATORS[_LOOKUP[key]] = getValidator(key, addon_config["schema"][key])

_VALIDATORS[Setting.MAX_SYNC_INTERVAL_SECONDS] = DurationAsSecondsValidator("max_sync_interval_seconds", 1, None)
VERSION = addon_config["version"]
