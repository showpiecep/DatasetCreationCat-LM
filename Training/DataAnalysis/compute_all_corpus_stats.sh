language=python
in_file=python-top-repos.txt
# python3 gh_crawler.py python # done executing
head -28350 $in_file | xargs -P32 -n1 -I% bash -c 'echo %; \
github_link=%; \
./compute_corpus_stats.sh $github_link '$language