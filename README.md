# AI_final

>Team Members: 孫宜君、楊竺耘、陳宥安  
>Interface reference: [Minesweeper](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper)
---
## About us
### Algorithm and Strategy
* Algorithm we used
    * Straightforward Algorithm
        * 詳見我們製作的[Notion筆記](https://satin-palladium-f05.notion.site/AI-Final-Project-8c83c190075d4c9ba224e807e6b106a9)
    * Expected value of being mines
        * 首先遍尋周圍的點，並且將這次遍尋的點的出現頻率紀錄在cell-freq中，接著再將這些點的周圍也遍尋一次，計算出周圍沒有走過的點的數量，紀錄於neighbor-num;將該點的周圍地雷數除以neighbor-num，並且採持續累加，最後再除以該點出現的頻率，如此便計算出該點的期望值。
* Strategy
    * Straigntforward Algorithm + Expected value
        * Judge the safe spots by Straightforward Algoreihm 
        * Calculate the expected value of the grids where are connected to the opened spots.
        * If there is safe spot, open it (randomly choose one if there are multiple safe spots).
        * Otherwise, choose the spot with lowest expected value (randomly choose one if there are multiple spots that have same expected value).
---
## About code
### Prerequisite
* Package you need:  
    * pygame  
* You can download the needed package by  
    ```shell=
    pip3 install -r requirements.txt
    ```
    or 
    ```shell=
    pip3 install pygame
    ```

### Start 
* You can start the game by running:
    ```shell=
    python3 runner.py
    ```
    and press the button "Play Game". Then you will see the game interface.
### Modes
* Manual Mode  
    * Simply start the game by clicking the grid with left mouse button.
    * You can mark the grid by clicking the grid with RIGHT mouse button. Pressing RIGHT mouse button again can numark the grid.
* AI move  
    * The AI we wrote will **move a step** for you based on the knowledge database the AI abtained.
* Autoplay  
    * The AI we wrote will **play a round** for you and display the result (win or loss).
* Test  
    * The AI we wrote will **run 10000 rounds** for you and display the following infomation:  
        * Won rate
        * Average step (if loss)
        * Total random step
        * Average score
        * Average score (if loss)
        you can change the time of running round in [runner.py](runner.py).  
---     
## Demo
* Video link: https://www.youtube.com/watch?v=Gzj6q7J6lxc&ab_channel=%E9%99%B3%E5%AE%A5%E5%AE%89

