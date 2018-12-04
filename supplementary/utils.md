## References

For some reason I couldn't find an easy (or any) way to include bibliographies into
my mkdoc sites.

This is what I did

```
pandoc -o docs/methods.html --bibliography=supplementary/RNAsik.bib docs/methods.md 
```

And then simply manually include `methods.html` content into `docs/index.md` file
It works, and that part of the markdown should really change that much
