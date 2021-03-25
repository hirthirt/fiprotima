import json
import random

from Model.util import log_message
from Model.EdgeModel.JSON.base import (
    BaseJSONHandler,
    BaseJSONClass,
    BaseAttribute,
    Caretaker,
    OTHER,
    DT_SEC,
    DT_SIMPLE_STRING,
    DT_WEBKIT,
    DT_WEBKIT_SEC,
    DT_SEC_DOT_MICRO
)

ACCTRKUPDATE = "Account Tracker Update"
NOTIFSERVICEFIRSTRUN = "Benachrichtigungsservice"
DEFBROLASTDECLINED = "Letzte Standardbrowser Ablehnung"
LASTUPDATE = "Letztes Update"
LASTREPORT = "Letzte Meldung"
EXTSIGEXPIRE = "Gültigkeit Erweiterungssignatur"
EXTSIGTIME = "Erweiterungssignatur Zeitstempel"
GAIACOOKIECHANGED = "Gaia-Cookie geändert"
PROFILECREATED = "Profil erstellt"
PROFILEENGAGEMENT = "Letzte Nutzung"
LASTCREDREMOVED = "Anmeldedaten entfernt"
LASTSAFEBROWSLOGTIME = "Letzter Safebrowsing-Log"




class Profile(BaseJSONClass):
    def __init__(self, account_tracker_service_update, 
                notification_service_first_run, default_browser_declined,
                last_update, domain_diversity_last_reporting,
                extension_sig_expire, extension_sig_timestamp,
                gaia_cookie_changed, profile_create_time,
                profile_last_engagement, profile_last_credential_remove,
                safebrowsing_last_log
        ):
        if account_tracker_service_update:
            self.account_tracker_service_update = int(account_tracker_service_update)
        else:
            self.account_tracker_service_update = account_tracker_service_update
        if notification_service_first_run:
            self.notification_service_first_run = int(notification_service_first_run)
        else:
            self.notification_service_first_run = notification_service_first_run
        if default_browser_declined:
            self.default_browser_declined = int(default_browser_declined)
        else:
            self.default_browser_declined = default_browser_declined
        if last_update:
            self.last_update = int(last_update)
        else:
            self.last_update = last_update
        if domain_diversity_last_reporting:
            self.domain_diversity_last_reporting = int(domain_diversity_last_reporting)
        else:
            self.domain_diversity_last_reporting = domain_diversity_last_reporting
        if extension_sig_expire:
            self.extension_sig_expire = extension_sig_expire
        else:
            self.extension_sig_expire = extension_sig_expire
        if extension_sig_timestamp:
            self.extension_sig_timestamp = int(extension_sig_timestamp)
        else:
            self.extension_sig_timestamp = extension_sig_timestamp
        if gaia_cookie_changed:
            self.gaia_cookie_changed = gaia_cookie_changed
        else:
            self.gaia_cookie_changed = gaia_cookie_changed
        if profile_create_time:
            self.profile_create_time = int(profile_create_time)
        else:
            self.profile_create_time = profile_create_time
        if profile_last_engagement:
            self.profile_last_engagement = int(profile_last_engagement)
        else:
            self.profile_last_engagement = profile_last_engagement
        if profile_last_credential_remove:
            self.profile_last_credential_remove = profile_last_credential_remove
        else:
            self.profile_last_credential_remove = profile_last_credential_remove
        if safebrowsing_last_log:
            self.safebrowsing_last_log = int(safebrowsing_last_log)
        else:
            self.safebrowsing_last_log = safebrowsing_last_log
        

        self.init()

    def init(self):
        self.is_date_changed = False
        self.id = random.randint(0,99)
        self.attr_list = []
        if self.profile_create_time:
            self.attr_list.append(BaseAttribute(PROFILECREATED, DT_WEBKIT, self.profile_create_time))
        if self.profile_last_engagement:
            self.attr_list.append(BaseAttribute(PROFILEENGAGEMENT, DT_WEBKIT, self.profile_last_engagement))
        if self.profile_last_credential_remove:
            self.attr_list.append(BaseAttribute(LASTCREDREMOVED, DT_SEC_DOT_MICRO, self.profile_last_credential_remove))
        if self.account_tracker_service_update:
            self.attr_list.append(BaseAttribute(ACCTRKUPDATE, DT_WEBKIT, self.account_tracker_service_update))
        if self.notification_service_first_run:
            self.attr_list.append(BaseAttribute(NOTIFSERVICEFIRSTRUN, DT_WEBKIT, self.notification_service_first_run))
        if self.default_browser_declined:
            self.attr_list.append(BaseAttribute(DEFBROLASTDECLINED, DT_WEBKIT, self.default_browser_declined))
        if self.last_update:
            self.attr_list.append(BaseAttribute(LASTUPDATE, DT_WEBKIT, self.last_update))
        if self.domain_diversity_last_reporting:
            self.attr_list.append(BaseAttribute(LASTREPORT, DT_WEBKIT, self.domain_diversity_last_reporting))
        if self.extension_sig_expire:
            self.attr_list.append(BaseAttribute(EXTSIGEXPIRE, DT_SIMPLE_STRING, self.extension_sig_expire))
        if self.extension_sig_timestamp:
            self.attr_list.append(BaseAttribute(EXTSIGTIME, DT_WEBKIT, self.extension_sig_timestamp))
        if self.gaia_cookie_changed:
            self.attr_list.append(BaseAttribute(GAIACOOKIECHANGED, DT_SEC_DOT_MICRO, self.gaia_cookie_changed))
        if self.safebrowsing_last_log:
            self.attr_list.append(BaseAttribute(LASTSAFEBROWSLOGTIME, DT_WEBKIT_SEC, self.safebrowsing_last_log))
        


    def update(self, delta):
        if not delta:
            log_message("Kein Delta erhalten in Profil", "error")
            return
        for attr in self.attr_list:
            if attr.name == PROFILECREATED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.profile_create_time = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == PROFILEENGAGEMENT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.profile_last_engagement = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTCREDREMOVED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.profile_last_credential_remove = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == ACCTRKUPDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.account_tracker_service_update = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == NOTIFSERVICEFIRSTRUN:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.notification_service_first_run = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == DEFBROLASTDECLINED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.default_browser_declined = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTUPDATE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.last_update = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTREPORT:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.domain_diversity_last_reporting = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == EXTSIGEXPIRE:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.extension_sig_expire = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == EXTSIGTIME:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.extension_sig_timestamp = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == GAIACOOKIECHANGED:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.gaia_cookie_changed = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True
            if attr.name == LASTSAFEBROWSLOGTIME:
                try:
                    attr.change_date(delta)
                    attr.date_to_timestamp()
                    self.safebrowsing_last_log = attr.timestamp
                except:
                    log_message("Fehler bei Update in Profil für " + attr.name, "error")
                    continue
                self.is_date_changed = True


class ProfileHandler(BaseJSONHandler):
    name = "Profile"

    profile = []
    json_all = dict

    def __init__(
        self, profile_path: str, file_name: str = "Preferences",
    ):
        super().__init__(profile_path, file_name)

    def get_all_id_ordered(self):
        if self.profile:
            return self.profile

        self.profile = []
        self.open_file()
        self.json_all = json.loads(self.read_file())
        self.close()

        try:
            account_tracker_service_update = self.json_all[
                "account_tracker_service_last_update"
            ]
        except:
            account_tracker_service_update = None

        try:
            notification_service_first_run = self.json_all[
                "announcement_notification_service_first_run_time"
            ]
        except:
            notification_service_first_run = None
        
        
        try:
            default_browser_declined = self.json_all["browser"][
                "default_browser_infobar_last_declined"
            ]
        except:
            default_browser_declined = None
        
        try:
            last_update = self.json_all["data_reduction"]["last_update_date"]
        except:
            last_update = None
        
        try:
            domain_diversity_last_reporting = self.json_all["domain_diversity"][
                "last_reporting_timestamp"
            ]
        except:
            domain_diversity_last_reporting = None
        
        try:
            extension_sig_expire = self.json_all["extensions"]["install_signature"][
                "expire_date"
            ]
        except:
            extension_sig_expire = None

        try:
            extension_sig_timestamp = self.json_all["extensions"]["install_signature"][
                "timestamp"
            ]
        except:
            extension_sig_timestamp = None

        try:
            gaia_cookie_changed = self.json_all["gaia_cookie"]["changed_time"]
        except:
            gaia_cookie_changed = None
        
        try:
            profile_create_time = self.json_all["profile"]["creation_time"]
        except:
            profile_create_time = None
        
        try:
            profile_last_engagement = self.json_all["profile"]["last_engagement_time"]
        except:
            profile_last_engagement = None
        
        try:
            profile_last_credential_remove = self.json_all["profile"][
                "last_time_obsolete_http_credentials_removed"
            ]
        except:
            profile_last_credential_remove = None
        
        try:
            safebrowsing_last_log = self.json_all["safebrowsing"]["metrics_last_log_time"]
        except:
            safebrowsing_last_log = None

        profile = Profile(account_tracker_service_update, notification_service_first_run,
                            default_browser_declined, last_update, domain_diversity_last_reporting,
                            extension_sig_expire, extension_sig_timestamp, gaia_cookie_changed, 
                            profile_create_time, profile_last_engagement, profile_last_credential_remove,
                            safebrowsing_last_log)
        self.caretakers.append(Caretaker(profile))
        self.profile.append(profile)
            

        return self.profile

    def commit(self):
        
        if self.profile[0].account_tracker_service_update:
            self.json_all[
                    "account_tracker_service_last_update"
                ] = self.profile[0].account_tracker_service_update
        
        if self.profile[0].notification_service_first_run:
            self.json_all[
                    "announcement_notification_service_first_run_time"
                ] = self.profile[0].notification_service_first_run
        
        if self.profile[0].default_browser_declined:
            self.json_all["browser"][
                    "default_browser_infobar_last_declined"
                ] = self.profile[0].default_browser_declined
        
        if self.profile[0].last_update:
            self.json_all["data_reduction"][
                "last_update_date"] = self.profile[0].last_update

        if self.profile[0].domain_diversity_last_reporting:
            self.json_all["domain_diversity"][
                    "last_reporting_timestamp"
                ] = self.profile[0].domain_diversity_last_reporting

        if self.profile[0].extension_sig_expire:
            self.json_all["extensions"]["install_signature"][
                    "expire_date"
                ] = self.profile[0].extension_sig_expire

        if self.profile[0].extension_sig_timestamp:
            self.json_all["extensions"]["install_signature"][
                    "timestamp"
                ] = self.profile[0].extension_sig_timestamp

        if self.profile[0].gaia_cookie_changed:
            self.json_all["gaia_cookie"]["changed_time"] = self.profile[0].gaia_cookie_changed

        if self.profile[0].profile_create_time:
            self.json_all["profile"]["creation_time"] = self.profile[0].profile_create_time

        if self.profile[0].profile_last_engagement:
            self.json_all["profile"]["last_engagement_time"] = self.profile[0].profile_last_engagement

        if self.profile[0].profile_last_credential_remove:
            self.json_all["profile"][
                    "last_time_obsolete_http_credentials_removed"
                ] = self.profile[0].profile_last_credential_remove

        if self.profile[0].safebrowsing_last_log:
            self.json_all["safebrowsing"][
                "metrics_last_log_time"] = self.profile[0].safebrowsing_last_log

        self.write_file()

        super().commit()
