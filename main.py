#Troy Tural 404
#TP5
import random

import arcade

# import arcade.gui

from AttackAnimation import AttackType, AttackAnimation
from game_state import GameState

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.


class MyGame(arcade.Window):

    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player = None
        self.computer = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.player_score = 0
        self.computer_score = 0
        self.computer_attack_type = None
        self.computer_attack_sprite = None
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = None
        self.gameResults = None

    def setup(self):
        """
        Ceci va permtrre au sprites d'etres les dimensions choisis chaque fois que le jeu commence. 
       """
        self.game_state = GameState.NOT_STARTED
        self.player = arcade.Sprite("Assets/faceBeard.png", 0.5, center_x=200, center_y=350)
        self.computer = arcade.Sprite("Assets/compy.png", 2.40, center_x=800, center_y=350)

        self.rock = AttackAnimation(AttackType.Rock)
        self.rock.center_x = 200
        self.rock.center_y = 150

        self.paper = AttackAnimation(AttackType.Paper)
        self.paper.center_x = 300
        self.paper.center_y = 150

        self.scissors = AttackAnimation(AttackType.Scissors)
        self.scissors.center_x = 400
        self.scissors.center_y = 150

    def victory_logic(self):

        if self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Rock:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Paper:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Rock and self.computer_attack_type == AttackType.Scissors:
            return "Win"

        if self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Paper:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Scissors:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Paper and self.computer_attack_type == AttackType.Rock:
            return "Win"

        if self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Scissors:
            return "Draw"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Rock:
            return "Loss"
        elif self.player_attack_chosen == AttackType.Scissors and self.computer_attack_type == AttackType.Paper:
            return "Win"

    def draw_possible_attack(self):  
        arcade.draw_rectangle_outline(
            200,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            300,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            400,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            825,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))
        
        if self.player_attack_chosen == AttackType.Rock:
            self.rock.draw()
        elif self.player_attack_chosen == AttackType.Paper:
            self.paper.draw()
        elif self.player_attack_chosen == AttackType.Scissors:
            self.scissors.draw()
        else:
            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()
        
    def validate_victory(self):
        
        attack_index = random.randint(0, 2)
        if attack_index == 0:
            self.computer_attack_type = AttackType.Rock
            self.computer_attack_sprite = AttackAnimation(AttackType.Rock)
        elif attack_index == 1:
            self.computer_attack_type = AttackType.Paper
            self.computer_attack_sprite = AttackAnimation(AttackType.Paper)
        elif attack_index == 2:
            self.computer_attack_type = AttackType.Scissors
            self.computer_attack_sprite = AttackAnimation(AttackType.Scissors)

        playerResults = self.victory_logic()

        if playerResults:
            self.game_state = GameState.ROUND_DONE

        if playerResults == "Win":
            self.player_score += 1
            self.gameResults = "Win"
            
        elif playerResults == "Loss":
            self.computer_score += 1
            self.gameResults = "Loss"

        elif playerResults == "Draw":
            self.gameResults = "Draw"

        if self.player_score == 3 or self.computer_score == 3:
            self.game_state = GameState.GAME_OVER

    def draw_computer_attack(self):
        if self.computer_attack_sprite:
            self.computer_attack_sprite.center_x = 825
            self.computer_attack_sprite.center_y = 150
            self.computer_attack_sprite.draw()

    def draw_text(self):
        """
       Dépendemment de l'état de jeu, l'ecran va afficher le texte approprie.
       """
        
        arcade.draw_text("Ton score s'agit de:" + str(self.player_score),
            -220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        arcade.draw_text("Le score de l'ordi s'agit de:" + str(self.computer_score),
            220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        string = None

        arcade.draw_text("Ton score s'agit de:" + str(self.player_score),
            -220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")
        
        arcade.draw_text("Le score de l'ordi s'agit de:" + str(self.computer_score),
            220,
            20,
            arcade.color.BLACK,
            20,
            width=SCREEN_WIDTH,
            align="center")

        if self.game_state == GameState.GAME_OVER:
            if self.player_score > self.computer_score: 
                string = "Victoire! Appuyer sur espace pour refaire une partie !"
            else:
                string = "Defaite! Appuyer sur espace pour refaire une partie !"

        elif self.game_state == GameState.NOT_STARTED:
            string = "Appuyer sur SPACE pour commencer une nouvelle partie !"
        elif self.game_state == GameState.ROUND_ACTIVE:
            string = "Cliquez sur une image pour jouer !"
        elif self.game_state == GameState.ROUND_DONE:
            if self.gameResults == "Win":
                string = "YOU WIN! Appuyer sur SPACE pour jouer une autre ronde !"
            elif self.gameResults == "Loss":
                string = "Perdu, Appuyer sur SPACE pour jouer une autre ronde !"
            elif self.gameResults == "Draw":
                string = "DRAW ! Appuyer sur SPACE pour jouer une autre ronde !"
        

        arcade.draw_text(string,
            350,
            300,
            arcade.color.BLACK,
            20,
            width=300,
            align="center",)
        
    def on_draw(self):
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.player.draw()
        self.computer.draw()

        self.draw_computer_attack()

        self.draw_text()
        self.draw_possible_attack()

    def on_update(self, delta_time):

        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update()
            self.paper.on_update()
            self.scissors.on_update()   

    def on_key_press(self, key, key_modifiers):
        """on_key_press va faire en sorte que l'ordi va reconaitre les touches du clavier."""
        if key == 32:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.ROUND_DONE:
                self.game_state = GameState.ROUND_ACTIVE
                self.gameResults = None
                self.computer_attack_sprite = None
                self.player_attack_chosen = None

            elif self.game_state == GameState.GAME_OVER:
                self.game_state = GameState.ROUND_ACTIVE
                self.player_score = 0
                self.computer_score = 0
                self.computer_attack_type = None
                self.player_attack_chosen = False
                self.draw_round = None

    def on_mouse_press(self, x, y, button, key_modifiers):

        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x,y)):
                self.player_attack_chosen = AttackType.Rock
                self.validate_victory()

            elif self.paper.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Paper
                self.validate_victory()

            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.Scissors
                self.validate_victory()

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
   main()

