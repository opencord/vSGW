# Virtual Serving Gateway Service

## Onboarding

To onboard this service in your system, you can add the service to the `mcord.yml` profile manifest:

```
xos_services:
  - name: vsgw
    path: orchestration/xos_services/vsgw
    keypair: mcord_rsa
    synchronizer: true
```

Once you have added the service, you will need to rebuilt and redeploy the XOS containers from source. Login to the `corddev` vm and `cd /cord/build`

```
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml PIprepPlatform
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :platform-install:buildImages
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :platform-install:publish
$ ./gradlew -PdeployConfig=config/mcord_in_a_box.yml :orchestration:xos:publish
```

Now the new XOS images should be published to the registry on `prod`. To bring them up, login to the `prod` VM and define these aliases:

```
$ CORD_PROFILE=$( cat /opt/cord_profile/profile_name )
$ alias xos-pull="docker-compose -p $CORD_PROFILE -f /opt/cord_profile/docker-compose.yml pull"
$ alias xos-up="docker-compose -p $CORD_PROFILE -f /opt/cord_profile/docker-compose.yml up -d --remove-orphans"
$ alias xos-teardown="pushd /opt/cord/build/platform-install; ansible-playbook -i inventory/head-localhost --extra-vars @/opt/cord/build/genconfig/config.yml teardown-playbook.yml; popd"
$ alias compute-node-refresh="pushd /opt/cord/build/platform-install; ansible-playbook -i /etc/maas/ansible/pod-inventory --extra-vars=@/opt/cord/build/genconfig/config.yml compute-node-refresh-playbook.yml; popd"
```

To pull new images from the database and launch the containers, while retaining the existing XOS database, run:

```
$ xos-pull; xos-up
```

Alternatively, to remove the XOS database and reinitialize XOS from scratch, run:

```
$ xos-teardown; xos-pull; xos-launch; compute-node-refresh
```
