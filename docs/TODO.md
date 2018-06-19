# ToDo

- turns out that picard that comes with conda install isn't good for clusters env.
there might be a simple fix to this, but basically this to do to remind me to DO that.
This is all to do with not having enough heap memory, I think the fix might be as simple
as setting sik.config to have

```
picardExe = pirad -Xmx6g
```

From reading condas picard wrapper script it appears that I can just pass extra java args
through like that, needs testing

document RNASIK_BDS_CONFIG and do travi test
