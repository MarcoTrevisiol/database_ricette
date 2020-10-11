#!/bin/dash

working_dir=/var/local/database_ricette
# localization of units

# installation of services
ln -sf "${working_dir}/telegram_bot/RicettePersonaliBot.service" "/etc/systemd/system"
ln -sf "${working_dir}/web_ui/SiteSetup.service" "/etc/systemd/system"

# activation of services
systemctl daemon-reload
systemctl enable RicettePersonaliBot
systemctl enable SiteSetup

systemctl start RicettePersonaliBot
systemctl start SiteSetup

