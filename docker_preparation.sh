read -s -p "Github access token: " github
echo
read -s -p "Telegram bot token: " telegram
echo
catalogo_path=catalogo
www_path="${PWD%/*}/htdocs"

git clone "https://github.com/MarcoTrevisiol/database_ricette_solo_catalogo.git" "${catalogo_path}"
git --git-dir="${catalogo_path}/.git" config credential.helper 'store --file=.git/cre'
chmod a+w "${catalogo_path}/catalogo_ricette.json"
printf "https://MarcoTrevisiol:${github}@github.com\n" >"${catalogo_path}/.git/cre"
printf "CATALOGO_PATH=${PWD}/${catalogo_path}\nTOKEN=${telegram}\nWWW_PATH=${www_path}\n" >.env
for docker_image in docker_image*.tar
do
  docker load <"${docker_image}"
done

