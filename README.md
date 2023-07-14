# atari_ai_controller
AI controller for Atari emulator using body positions (via depth camera) and muscle contraction (via EMG sensors).


## Setup

Use "pip install ." to setup the package and its dependencies.


## Cheat sheet

### Windows version

1. Setup configs file
```
src\configs\__init__.py
```

2. Prepare pose classifier
    1. Collect poses for the five conditions
    ```
    python src\pose\record_pose.py --condition rest --duration 30 --skel 0
    python src\pose\record_pose.py --condition left --duration 30 --skel 0
    python src\pose\record_pose.py --condition right --duration 30 --skel 0
    python src\pose\record_pose.py --condition up --duration 30 --skel 0
    python src\pose\record_pose.py --condition down --duration 30 --skel 0
    ```

    2. Extract features and merge conditions
    ```
    python src\pose\prepare_train_poses.py
    ```

    3. Train pose classifier
    ```
    "python src\ai\train_model.py --type pose --model svm --train_and_evaluate True
    ```

3. Prepare emg classifier
    1. Collect emg for the two conditions
    ```
    python src\emg\record_emg.py --condition rest --duration 30
    python src\emg\record_emg.py --condition fire --duration 30
    ```

    2. Extract features and merge conditions
    ```
    python src\emg\prepare_train_emg.py --window 250
    ```

    3. Train emg classifier
    ```
    python src\ai\train_model.py --type emg --model svm --train_and_evaluate True
    ```
4. Run pose and emg controlled in parallel
Two modes are possible here: local (emulator is running in my pc) or remote (emulator is running in another pc)

*Local version:*
```
python src\pose\run_pose_controller.py --model svm --skel 0 --ip 127.0.0.1
python src\emg\run_emg_controller.py --model svm --window 250 --ip 127.0.0.1
```

*Remote version:*
```
python src\pose\run_pose_controller.py --model svm --skel 0
python src\emg\run_emg_controller.py --model svm --window 250 
```

### For running the game engine on my pc

```
python3 src/emulator/game_engine.py --atari_ip 127.0.0.1
```


### Mac OS version

1. Setup configs file
```
src/configs/__init__.py
```

2. Prepare pose classifier
    1. Collect poses for the five conditions
    ```
    python3 src/pose/record_pose.py --condition rest --duration 30 --skel 0
    python3 src/pose/record_pose.py --condition left --duration 30 --skel 0
    python3 src/pose/record_pose.py --condition right --duration 30 --skel 0
    python3 src/pose/record_pose.py --condition up --duration 30 --skel 0
    python3 src/pose/record_pose.py --condition down --duration 30 --skel 0
    ```

    2. Extract features and merge conditions
    ```
    python3 src/pose/prepare_train_poses.py
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

Two modes are possible here: local (emulator is running in my pc) or remote (emulator is running in another pc)

*Local version:*
```
python3 src/pose/run_pose_controller.py --model svm --skel 0 --ip 127.0.0.1
python3 src/emg/run_emg_controller.py --model svm --window 250 --ip 127.0.0.1
```

*Remote version:*
```
python3 src/pose/run_pose_controller.py --model svm --skel 0
python3 src/emg/run_emg_controller.py --model svm --window 250 
```

### For running the game engine on my pc

```
python3 src/emulator/game_engine.py --atari_ip 127.0.0.1
```


## IMPORTANT!

Always run ``` pip install . ``` after each code change!
