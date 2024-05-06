#!/bin/bash

usage() {
    echo "  options:"
    echo "      -b: launch behavior tree"
    echo "      -t: launch keyboard teleoperation"
    echo "      -n: n drones, default is 1"
    echo "      -p: n drones, default is 1"
    echo "      -r: n drones, default is 1"
}

# Arg parser
while getopts "n:p:r:brt" opt; do
  case ${opt} in
    b )
      behavior_tree="true"
      ;;
    t )
      launch_keyboard_teleop="true"
      ;;
    n )
      num_drones=${OPTARG}
      ;;
    p )
      num_panels=${OPTARG}
      ;;
    r )
      num_rows=${OPTARG}
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      usage
      exit 1
      ;;
    : )
      if [[ ! $OPTARG =~ ^[wrt]$ ]]; then
        echo "Option -$OPTARG requires an argument" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

source utils/tools.bash

# Shift optional args
shift $((OPTIND -1))

## DEFAULTS
behavior_tree=${behavior_tree:="false"}
swarm=${swarm:="false"}
record_rosbag="false"
launch_keyboard_teleop=${launch_keyboard_teleop:="false"}
drone_namespace="drone"

export GZ_SIM_RESOURCE_PATH=$PWD/assets/worlds:$PWD/assets/models:$GZ_SIM_RESOURCE_PATH

echo $num_drones

python3 scripts/world_customizer.py $num_drones $num_panels $num_rows

simulation_config="assets/worlds/solar_field.json"

# Generate the list of drone namespaces
drone_ns=()
for ((i=0; i<${num_drones}; i++)); do
  drone_ns+=("$drone_namespace$i")
done

for ns in "${drone_ns[@]}"
do
  tmuxinator start -n ${ns} -p tmuxinator/session.yml drone_namespace=${ns} simulation_config=${simulation_config} behavior_tree=${behavior_tree} &
  wait
done

if [[ ${record_rosbag} == "true" ]]; then
  tmuxinator start -n rosbag -p tmuxinator/rosbag.yml drone_namespace=$(list_to_string "${drone_ns[@]}") &
  wait
fi

if [[ ${launch_keyboard_teleop} == "true" ]]; then
  tmuxinator start -n keyboard_teleop -p tmuxinator/keyboard_teleop.yml simulation=true drone_namespace=$(list_to_string "${drone_ns[@]}") &
  wait
fi

tmuxinator start -n gazebo -p tmuxinator/gazebo.yml simulation_config=${simulation_config} &
wait

# Attach to tmux session ${drone_ns[@]}, window mission
tmux attach-session -t ${drone_ns[0]}:mission
