#! /bin/sh
echo "Relay Service"
sudo cp ./SeRAPiS_Relay.service /etc/systemd/system/SeRAPiS_Relay.service
echo "Sensor Service"
sudo cp ./SeRAPiS_Sensor.service /etc/systemd/system/SeRAPiS_Sensor.service
echo "reload Services"
sudo systemctl daemon-reload
echo ""
#TODO - Menu to select Services that need installing
for i in "SeRAPiS_Relay.service" "SeRAPiS_Sensor.service"
do
  echo "start $i Service"
  sudo systemctl start $i
  echo "enable $i Service to start on boot"
  sudo systemctl enable $i
  echo "Status $i Service"
  sudo systemctl status $i
  echo
  echo
done