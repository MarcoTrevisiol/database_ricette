pattern=<!-- App scripts -->

index.html: index_model.html main.js
	sed "s|${pattern}|<script src=\"main.js\"></script>|" <$< >$@

main.js: static/main.js static/*.js static/*/*.js
	cat $^ >$@

clean:
	-rm index.html main.js

.PHONY: clean
