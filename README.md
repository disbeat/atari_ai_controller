# atari_ai_controller
AI controller for Atari emulator using body positions (via depth camera) and muscle contraction (via EMG sensors).


## Setup

Use "pip install ." to setup the package and its dependencies.


## Cheat sheet
1. Setup configs file
```
src/configs/__init__.py
```

2. Prepare pose classifier
    1. Collect poses for the five conditions
    ```
    python3 src/pose_tracker/record_poses.py --condition rest --duration 30 --skel 0
    python3 src/pose_tracker/record_poses.py --condition left --duration 30 --skel 0
    python3 src/pose_tracker/record_poses.py --condition right --duration 30 --skel 0
    python3 src/pose_tracker/record_poses.py --condition up --duration 30 --skel 0
    python3 src/pose_tracker/record_poses.py --condition down --duration 30 --skel 0
    ```

    2. Extract features and merge conditions
    ```
    python3 src/pose_tracker/prepare_train_poses.py
    ```

    3. Train pose classifier
    ```
    "python3 src/ai/train_model.py --type pose --model svm --train_and_evaluate True
    ```

3. Prepare emg classifier
    1. Collect emg for the two conditions
    ```
    python3 src/emg/record_emg.py --condition rest --duration 30
    python3 src/emg/record_emg.py --condition fire --duration 30
    ```

    2. Extract features and merge conditions
    ```
    python3 src/emg/prepare_train_emg.py --window 250
    ```

    3. Train emg classifier
    ```
    python3 src/ai/train_model.py --type emg --model svm --train_and_evaluate True
    ```
4. Run pose and emg controlled in parallel
```
python3 src/pose_tracker/run_pose_controller.py --model svm --skel 0
python3 src/emg/run_emg_controller.py --model svm --window 250
```

## IMPORTANT!

Always run ``` pip install . ``` after each code change!
