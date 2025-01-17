from util.utils import Region, Utils
from util.logger import Logger
from util.stats import Stats
from util.config import Config


class CommissionModule(object):

    def __init__(self, config, stats):
        """Initializes the Expedition module.

        Args:
            config (Config): ALAuto Config instance
            stats (Stats): ALAuto stats instance
        """
        self.enabled = True
        self.config = config
        self.stats = stats
        self.urgent_checked = False
        self.region = {
            'left_menu': Region(0, 203, 57, 86),
            'collect_oil': Region(206, 105, 98, 58),
            'collect_gold': Region(579, 102, 98, 58),
            'complete_commission': Region(574, 393, 181, 61),
            'button_go': Region(574, 393, 181, 61),
            'urgent_tab': Region(24, 327, 108, 103),
            'daily_tab': Region(22, 185, 108, 103),
            'last_commission': Region(298, 846, 1478, 146),
            'commission_recommend': Region(1306, 483, 192, 92),
            'commission_start': Region(1543, 483, 191, 92),
            'oil_warning': Region(1073, 738, 221, 59),
            'button_back': Region(48, 43, 76, 76)
        }

    def commission_logic_wrapper(self):
        while True:
            Utils.update_screen()

            if Utils.find("commission/alert_completed"):
                Logger.log_msg("Found commission completed alert.")
                Utils.touch_randomly(self.region["left_menu"])
                continue
            if Utils.find("commission/button_completed") and (lambda x:x > 332 and x < 511)(Utils.find("commission/button_completed").y):
                Logger.log_debug("Found commission complete button.")
                Utils.touch_randomly(self.region["collect_oil"])
                Utils.touch_randomly(self.region["collect_gold"])
                Utils.touch_randomly(self.region["complete_commission"])
                Utils.script_sleep(1)
                continue
            if Utils.find("commission/alert_perfect"):
                Utils.touch_randomly(Region(661, 840, 598, 203))
                self.stats.increment_commissions_received()
                continue
            if Utils.find("menu/item_found"):
                Utils.touch_randomly(Region(661, 840, 598, 203))
                Utils.script_sleep(1)
                continue
            if Utils.find("commission/alert_available") and (lambda x:x > 332 and x < 511)(Utils.find("commission/alert_available").y):
                Logger.log_debug("Found commission available indicator.")
                Utils.touch_randomly(self.region["button_go"])
                continue
            if Utils.find("commission/button_go"): 
                Logger.log_msg("All commissions are running.")
                Utils.touch_randomly(Region(970, 148, 370, 784))
                return True
            while Utils.find("menu/commission"):
                Utils.update_screen() 

                if Utils.find("commission/alert_begun"):
                    Logger.log_msg("Successfully started commission.")
                    Utils.touch_randomly(Region(688, 11, 538, 55))
                    Utils.script_sleep(1)
                    self.stats.increment_commissions_started()
                    continue
                if Utils.find("commission/button_confirm"):
                    Logger.log_debug("Found commission oil warning message.")
                    Utils.touch_randomly(self.region["oil_warning"])
                    continue
                if Utils.find("commission/commissions_full"):
                    Logger.log_msg("No more commissions to start.")
                    Utils.touch_randomly(self.region["button_back"])
                    Utils.script_sleep(1)
                    break
                if Utils.find("commission/button_complete"):
                    Logger.log_debug("Found commission start button.")
                    Utils.touch_randomly(self.region["commission_start"])
                    continue
                if Utils.find("commission/button_recommend"):
                    Logger.log_debug("Found commission recommend button.")
                    Utils.touch_randomly(self.region["commission_recommend"])
                    continue

                if self.urgent_checked == False:
                    Utils.touch_randomly(self.region["urgent_tab"])
                    Utils.update_screen()

                    if Utils.find_and_touch("commission/commission_status"):
                        Logger.log_msg("Found status indicator on urgent commission.")
                    else: 
                        Utils.script_sleep()
                        Utils.touch_randomly(self.region["daily_tab"])
                        Logger.log_msg("No urgent commissions.")
                        self.urgent_checked = True
                else:
                    Utils.swipe(960, 680, 960, 400, 80)
                    Utils.touch_randomly(self.region["last_commission"])
                    Logger.log_debug("Found status indicator on commission.")