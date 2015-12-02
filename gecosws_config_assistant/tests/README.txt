TEST ENVIRONMENT SETUP:
-----------------------
Necessary tools:
* schroot
* debootstrap


To perform the tests you will need a "schrooted" GECOS Linux environmet to access to:

 mkdir -p /srv/chroot/gecos
 debootstrap --arch i386  trusty /srv/chroot/gecos http://v2.gecos.guadalinex.org/ubuntu/
 
Then edit /etc/schroot/schroot.conf file and add the following lines:

    [trusty-gecos]
    description=Environment to test Gecos config assistant
    aliases=gecos
    type=plain
    directory=/srv/chroot/gecos
    users=jenkins
    root-groups=root
    personality=linux
    preserve-environment=true

After that, bind mount the necessary folders:

    mount -o bind /proc /srv/chroot/gecos/proc
    mount -o bind /dev /srv/chroot/gecos/dev
    mount -o bind /dev/pts /srv/chroot/gecos/dev/pts
    
Now bind mount your testing environment:

    cp gecosv2.list /srv/chroot/gecos/etc/apt/sources.list.d/
    rm /srv/chroot/gecos/etc/apt/sources.list 
    echo "#Sources in sources.list.d" > /srv/chroot/gecos/etc/apt/sources.list
    cp trusted.gpg /srv/chroot/gecos/etc/apt/
    
    schroot -c gecos
    apt-get update
    apt-get install python
    apt-get install python-distutils-extra
    apt-get install python-coverage
    apt-get install gecosws-meta
    adduser jenkins
    exit
    mount -o bind /home/jenkins /srv/chroot/gecos/home/jenkins
    
    