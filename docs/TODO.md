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

- add support for "transcript_level_support" into geneIds.txt file and propogate that through.
idea being that some genes have greater support (confidence) then others, perhaps would be nice
to see that but also filter on that i.e only "transcript_support_level = 1" best evidence (biological)
It looks like "transcript_support_level" applicable to transcript and given gene can have several once
so will need thing on best way to summarise that

## Java related issues

I need to start gather better logs. This is useful command to grab java version and args

```
java -version
# Picked up JAVA_TOOL_OPTIONS:
# Picked up _JAVA_OPTIONS: -Xmx512m -Xms64m
# java version "1.7.0_40"
OpenJDK Runtime Environment (IcedTea 2.4.1) (suse-3.41.1-x86_64)
OpenJDK 64-Bit Server VM (build 24.0-b50, mixed mode)
```

I think issue of passing in correct memory i.e memory passed to the task has to be the same as memmory
passed to JVM, can be solved with `_JAVA_OPTIONS` parameter.

Other couple of useful commands are

```
jps
jps -v
```

This is to list running java process and they flags

I don't know at this stage what would be better

```
sys _JAVA_OPTIONS=blah $picardExe ...
```
OR

Parse memory out of the config and set it globaly

Do I need this option? JAVA_OPTIONS="-Djava.io.tmpdir=$HOME/tmp"

#### Links

- https://stackoverflow.com/questions/28327620/difference-between-java-options-java-tool-options-and-java-opts
