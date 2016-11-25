## RNAsik-pipe website

`docs.md` is the main file that docs should be written in. The simply use `pandoc` to convert markdown into html. One extra step is required to add class and id to `<ul>` element. I haven't figured better way yet, let me know if you do.

```BASH
pandoc docs.md -S -s -c siimple/dist/siimple.css -t html5 --title=RNAsik-docs -o index.html 
perl -0777 -i -pe 's/ul/ul class="topnav" id="myTopnav"/' index.html                           
```
