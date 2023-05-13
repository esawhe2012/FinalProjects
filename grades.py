# Author Isai Rangel Turned in  05/12/2023
# This program was based off of the youtube video ---> https://www.youtube.com/watch?v=fw5HruQlTA4
# It was used with the help of some StackOverflow articles and Pyqt5 documentation for formating
# https://doc.qt.io/qtforpython-5/PySide2/QtGui/QFont.html
# https://stackoverflow.com/questions/42100394/how-to-align-children-in-a-qhboxlayout-left-center-and-right
# https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QMessageBox.html
# I also used the lectures and notes for references  .


import sys
import random
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, \
    QInputDialog, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
# ------------------
# Purpose:
# This program will allow a user to play Rock, Paper, Scissors against the 'computer;
# User will be able to continuously play games until user exits or selects Clear to start over
# -------------------

# Game Widget
class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rock Paper Scissors')
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: black;")
        self.GameLayout = QVBoxLayout()
        self.player_wins = 0
        self.computer_wins = 0
        # Create Scoreboard label and formatting
        self.score = Scoreboard(self)
        self.welcome_label = QLabel(' - MAN VS COMPUTER - ')
        self.welcome_label.setFont(QFont("Silom", 40))
        self.blink_timer = QTimer(self)     # Create timer for blinking label
        self.blink_timer.timeout.connect(self.blink_label)
        self.blink_timer.start(500)
        # Player username instruction, input and button formatting
        self.playerName_label = QLabel('ENTER PLAYER NAME:')      # Player Name Label
        self.playerName_label.setFont(QFont("Andale Mono", 20))
        self.playerName_input = QLineEdit(self)
        self.playerName_input.setFixedSize(200, 30)

        self.playerName_button = QPushButton('Enter')   # Player Name button
        self.playerName_button.setFixedSize(120, 60)
        self.playerName_button.setStyleSheet("QPushButton { color: white; background-color: #001F3F; }")
        self.playerName_button.setFont(QFont('Silom', 30))
        self.playerName_button.clicked.connect(self.set_player_name)
        # add widgets and alignment
        self.GameLayout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)
        self.GameLayout.addWidget(self.playerName_label, alignment=Qt.AlignCenter)
        self.GameLayout.addWidget(self.playerName_input, alignment=Qt.AlignCenter)
        self.GameLayout.addWidget(self.playerName_button, alignment=Qt.AlignCenter)
        # player choices formatting
        self.choice_label = QLabel('\nMAKE YOUR CHOICE!')   # Choice Label
        self.choice_label.setFont(QFont("Andale Mono", 20))

        self.rock_button = QPushButton('Rock')  # Choice Buttons
        self.paper_button = QPushButton('Paper')
        self.scissors_button = QPushButton('Scissors')

        self.rock_button.clicked.connect(lambda: self.play_game('Rock'))    # Choice Button-click
        self.paper_button.clicked.connect(lambda: self.play_game('Paper'))
        self.scissors_button.clicked.connect(lambda: self.play_game('Scissors'))
        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.rock_button)
        self.button_layout.addWidget(self.paper_button)
        self.button_layout.addWidget(self.scissors_button)
        self.GameLayout.addWidget(self.choice_label, alignment=Qt.AlignCenter)
        self.GameLayout.addLayout(self.button_layout)
        self.GameLayout.addWidget(self.score)
        self.setLayout(self.GameLayout)
        # Button style
        self.button_style(self.rock_button)
        self.button_style(self.paper_button)
        self.button_style(self.scissors_button)
        # Clear button formatting and click
        self.clear_button = QPushButton('Clear')
        self.clear_button.setFixedSize(120, 60)
        self.clear_button.setStyleSheet("QPushButton { color: white; background-color: #001F3F; }")
        self.clear_button.setFont(QFont('Silom', 30))
        self.clear_button.clicked.connect(self.clear, self.player_wins, self.computer_wins)
        self.GameLayout.addWidget(self.clear_button, alignment=Qt.AlignCenter)

        self.current_player_choice: str = None

    # Formatting of blinking label
    def blink_label(self) -> None:
        if self.welcome_label.styleSheet():
            self.welcome_label.setStyleSheet('')
        else:
            self.welcome_label.setStyleSheet('color: green')

    # Validate and take player name
    def set_player_name(self) -> None:
        player_name = self.playerName_input.text()
        if not re.match("^[a-zA-Z0-9]+$", player_name):
            QMessageBox.warning(self, 'Invalid Input', 'Username can only contain letters and numbers.')
            return

        if player_name:
            self.playerName_label.setText(f'Player Name: {player_name}')
            self.playerName_input.setDisabled(True)

    # Take player choice and play against computer choice
    def play_game(self, player_choice) -> None:
        if not self.playerName_input.text():
            QMessageBox.warning(self, 'Invalid Input', 'Please enter your name.')
            return

        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices) # Computer rndm choice generator

        result = self.get_winner(player_choice, computer_choice, self.playerName_input.text())

        if result == "You won!":    # result message of win or lose
            self.player_wins += 1
        elif result == "Computer won!":
            self.computer_wins += 1
        # update scoreboard
        self.score.update_score(result, player_choice, computer_choice, self.player_wins, self.computer_wins)
        self.score.show()

    # declare player choice and return if won
    def get_winner(self, player_choice, computer_choice, player_name) -> str:
        if player_choice == computer_choice:
            return f"It's a tie!"
        elif player_choice == 'Scissors' and computer_choice == 'Paper':
            return f"You won!"
        elif player_choice == 'Paper' and computer_choice == 'Rock':
            return f"You won!"
        elif player_choice == 'Rock' and computer_choice == 'Scissors':
            return f"You won!"
        else:
            return f"Computer won!"

    # button styling for uniformality
    def button_style(self, button) -> None:
        button.setStyleSheet(
            '''
            QPushButton {
                background-color: #f0f0f0;
                border-style: solid;
                border-width: 2px;
                border-radius: 50px;
                padding: 10px;
                min-width: 100px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e
            }
            ''')

    # Clear contents when player clicks, reset all input
    def clear(self):
        self.playerName_input.setDisabled(False)
        self.playerName_input.clear()
        self.playerName_label.setText('ENTER PLAYER NAME:')
        self.player_wins = 0
        self.computer_wins = 0
        self.score.clear_score()

    # Clear score
    def clear_score(self) -> None:
        self.score.clear_score()

# Scoreboard
class Scoreboard(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(550, 200)
        self.parent = parent
        # Scoreboard label, and formatting
        self.score_label = QLabel('- - - - SCOREBOARD - - - -')
        self.score_label.setFont(QFont("Andale Mono", 30))
        self.score_label.setStyleSheet("QLabel { color: yellow; }")
        self.score_list_label = QLabel('')

        scoreboard_widget = QWidget()  # Create a container widget
        scoreboard_widget.setFixedSize(500, 400)

        # Layout for score label and output
        self.layout = QVBoxLayout(scoreboard_widget)
        self.setLayout(self.layout)
        self.score_label.setFont(QFont("Silom", 20))  # Score Label
        self.score_label.setStyleSheet("QLabel { color: yellow; }")
        self.score_list_label.setFont(QFont("Silom", 14))  # Score ListLabel
        self.score_list_label.setStyleSheet("QLabel { color: yellow; }")
        self.layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.score_list_label, alignment=Qt.AlignCenter)

    # Updates Score with output
    def update_score(self, result, player_choice, computer_choice, player_wins, computer_wins):
        results_msg = f"You chose\t\t{player_choice} \nComputer chose\t\t{computer_choice}\n"
        results_msg += f"{result}\n"
        results_msg += f" \n"
        results_msg += f" \n"
        results_msg += f"\tPlayer wins: {player_wins}\n"
        results_msg += f"\tComputer wins: {computer_wins}\n"
        self.score_list_label.setText(results_msg)
    # clears score list contents
    def clear_score(self) -> None:
        self.score_list_label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())
