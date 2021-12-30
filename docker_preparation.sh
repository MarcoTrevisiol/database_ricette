read -s -p "Github access token: " github
echo
read -s -p "Telegram bot token: " telegram
echo
export CATALOGO_PATH=cata
export BOT_ENV=bot_env

git clone "https://github.com/MarcoTrevisiol/database_ricette_solo_catalogo.git" "${CATALOGO_PATH}"
git --git-dir="${CATALOGO_PATH}/.git" config credential.helper 'store --file=.git/cre'
chmod a+w "${CATALOGO_PATH}/catalogo_ricette.json"
printf "https://MarcoTrevisiol:${github}@github.com\n" >"${CATALOGO_PATH}/.git/cre"
printf "TOKEN=${telegram}\n" >"${BOT_ENV}"
printf "CATALOGO_PATH=${CATALOGO_PATH}\nBOT_ENV=${BOT_ENV}\n" >.env


