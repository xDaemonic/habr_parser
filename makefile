upload:
	 git add -A && git commit -m "local upload $(date '+%Y-%m-%d %H:%M:%S')" && git pull && git push
