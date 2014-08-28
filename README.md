README
=======

(C) 2014 Takahiro Yoshimura <altakey@gmail.com>.  All rights reserved.

Random gadgets for blogging on WordPress.

0. HOW TO USE
--------------

    $ /path/to/python-3.4/bin/pyvenv ~/ve/channer
    $ source ~/ve/channer
    (channer) $ easy_install /path/to/repos
    ...
    (channer) $ cat words.tsv
    Google Glass	http://www.google.com/glass/start/
    Android Wear	http://www.android.com/wear
    Android	http://www.android.com/
    Eclipse	http://www.eclipse.org/juno/
    Gradle	http://www.gradle.org/
    Android Studio	https://developer.android.com/sdk/installing/studio.html
    Ant	http://ant.apache.org/
    Maven	http://maven.apache.org/
    Activity	http://developer.android.com/guide/components/activities.html
    Service	http://developer.android.com/guide/components/services.html
    View	http://developer.android.com/reference/android/view/View.html
    Nexus 5	http://www.google.com/nexus/5/
    Nexus S	http://www.gsmarena.com/samsung_google_nexus_s-3620.php
    ...
    (channer) $ cat thoughts.txt
    Hello, [Google Glass], meet the [NEXUS FIVE|http://www.google.com/nexus/5/].

    (channer) $ resolve-links words.tsv < thoughts.txt
    Hello, <a href="http://www.google.com/glass/start/" title="Google Glass">Google Glass</a>, meet the <a href="http://www.google.com/nexus/5/" title="Nexus 5 - Google">NEXUS FIVE</a>.

1. FEATURES
-----------

 * Attempts to resolve links and titles

2. BUGS
--------

 * Insanely hackish.
