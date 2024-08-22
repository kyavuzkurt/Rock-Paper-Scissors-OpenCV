# Rock-Paper-Scissors-OpenCV
A Rock Paper Scissors game on webcam. Currently computer makes random guesses. In the future I plan to implement image processing algorithms to the hand detection to predict the future hand position. This aims to make computer make a predicted guess instead of random guess.


## How to play
1. Clone the repository
```
git clone https://github.com/kyavuzkurt/Rock-Paper-Scissors-OpenCV.git
```
2. Install the dependencies
```
pip install -r requirements.txt
```
3. Run the script
```
python main.py
```
4. Show your hand to the webcam and press space to start the game
5. The script will tell you if you won, lost, or tied   
6. Press q to quit the game


## Future Work
- [ ] Apply Kalman Filter and Optical Flow to the hand detection to predict the future hand position. This aims to make computer make a predicted guess instead of random guess.
- [ ] If Kalman Filter and Optical Flow doesn't give good results, try to build either a CNN or RNN model to predict the future hand position.

## License
This project is licensed under the MIT License - see the LICENSE file for details