# thachlam's project
# remmeber to read the readme

from settings import * 
from os.path import join

class drawTools:
    def __init__(self, logic_tools):
        self.win = pygame.display.get_surface()
        self.logic_tools = logic_tools

    def draw_question_bar(self):
        question_rect = pygame.Rect(WIDTH / 2 - QUESTION_WIDTH / 2, 250, QUESTION_WIDTH , QUESTION_HEIGHT)

        pygame.draw.rect(self.win, "white", question_rect)
        pygame.draw.polygon(self.win, "white", 
            ((question_rect.left, question_rect.y), 
            (question_rect.left - 50, question_rect.y + QUESTION_HEIGHT / 2), 
            (question_rect.left, question_rect.bottom),))

        pygame.draw.polygon(self.win, "white", 
            ((question_rect.right, question_rect.y), 
            (question_rect.right + 50, question_rect.y + QUESTION_HEIGHT / 2), 
            (question_rect.right, question_rect.bottom),))

        return question_rect

    def display_long_text(self, font, string, rect, max_length):
        
        # display text if it's just in a line
        text = FONT[font].render(string, True, "black")

        if len(string) <= max_length:
            self.win.blit(text, (rect.x + rect.width / 2 - text.get_width() / 2,
                                 rect.y + rect.height / 2 - text.get_height() / 2))


        # display question in another line if it's too long
        else:
            words = self.logic_tools.split_long_text(string, max_length)
            if len(words) == 3:
                words = self.logic_tools.split_long_text(string, max_length + 5)

            total_height = text.get_height() * len(words) + TEXT_GAP * (len(words) - 1)

            for i in range(len(words)):
                text = FONT[font].render(words[i], True, "black")

                self.win.blit(text, (rect.x + rect.width / 2 - text.get_width() / 2,
                    rect.y + rect.height / 2 - total_height / 2 + text.get_height() * i))


    def draw_end_game(self, text, image, resetGame):
        text = FONT['end'].render(text, True, "white")
        text_rect = text.get_rect()
        image = pygame.image.load(join("../images", image + ".png"))

        total_height = text_rect.height + image.get_height() - 20

        self.win.fill("black")
        self.win.blit(image, (WIDTH / 2 - image.get_width() / 2 + 20, text_rect.bottom))
        self.win.blit(text, (WIDTH / 2 - text_rect.width / 2, HEIGHT / 2 - total_height / 2))
        
        pygame.display.update()
        pygame.time.wait(3000)
        resetGame()

    def draw_end_game_with_state(self, state, leak_answer_timer, current_money, resetGame):
        if state == "lose":
            text = "Ohh! You lost all your money."

        elif state == "take-money":
            text = f"You won {MONEY_IN_STRING[current_money]} dollars!!! "

        elif state == "win":
            text = "You are now a millionaire!!!"
            
        self.draw_end_game(text, state, resetGame)


    def display_instructions(self, visible, current_money, correct_answer):
        if visible:
            text = FONT['instruction'].render("Shortcut: 'm': money board, 't': take money, 'h': support", True, "white")
            self.win.blit(text, (WIDTH / 2 - text.get_width() / 2, 0))
            
            text2 = FONT['instruction'].render("Press 's' to open or close shorcut instructions", True, "white")
            self.win.blit(text2, (WIDTH / 2 - text2.get_width() / 2, 40))

        else:
            # if dont display instruction then display money
            string = f"Question {correct_answer + 1}: {MONEY_IN_STRING[current_money]} $"
            text2 = FONT['question'].render(string, True, "black")
            
            x = WIDTH / 2 - text2.get_width() / 2
            y = SUPPORT_START_Y / 2 - text2.get_height() / 2 - 10
            
            pygame.draw.rect(self.win, "yellow", text2.get_rect(topleft = (x- 1, y)))
            self.win.blit(text2, (x, y))



class LogicTools:
    @staticmethod
    # split the text to multiple lines if its too long
    def split_long_text(string, max_length):
        words = [string]
        while len(words[-1]) > max_length:
            char = words[-1][max_length - 1]

            if char == " ":
                before = words[-1][0: max_length - 1]
                after = words[-1][max_length: ]
                words[-1] = before
                words.append(after)

            else:
                for i in range(max_length - 1, -1, -1):
                    if words[-1][i] == " ":
                        before = words[-1][0: i]
                        after = words[-1][i + 1: ]
                        words[-1] = before
                        words.append(after)
                        break

        return words


    # check if a support is used so when we move we can get over it
    @staticmethod
    def get_support_index(index, supports, direction):
        
        # there are four supports so i use range(4)
        for i in range(4): 
            index = (index + direction) % 4 

            if not supports[index].used:
                return index

    @staticmethod
    def get_answer_index(pos, move_x, move_y, question_set):
        if move_x:
            pos['col'] = (pos['col'] + move_x) % 2 

            if len(question_set) != 3:
                return

            # check if there just two answers left
            num = pos['col'] + pos['row'] * 2 
            if ANSWERS[num] not in question_set:
                num = pos['col'] + ((pos['row'] + 1) % 2) * 2 
                
                if ANSWERS[num] in question_set:
                    pos['row'] = (pos['row'] + 1) % 2
                else:
                    pos['col'] = (pos['col'] - move_x) % 2 


        else:
            pos['row'] = (pos['row'] + move_y) % 2 

            if len(question_set) != 3:
                return

            # check if there just two answers left
            num = pos['col'] + pos['row'] * 2 
            if ANSWERS[num] not in question_set:
                num = (pos['col'] + 1) % 2 + pos['row'] * 2 
                
                if ANSWERS[num] in question_set:
                    pos['col'] = (pos['col'] + 1) % 2
                else:
                   pos['row'] = (pos['row'] - move_y) % 2 

 

def get_answer_polygon_pos():
    all_pos = []
    total_width = ANSWER_WIDTH * 2 + ANSWER_GAP_X
    start_x = WIDTH / 2 - total_width / 2
    start_y = HEIGHT / 1.6

    for row in range(2):
        for col in range(2):
            pos = []
            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col + 50,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row))  

            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row + ANSWER_HEIGHT / 2))

            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col + 50,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row + ANSWER_HEIGHT))   

            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col + ANSWER_WIDTH - 50,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row + ANSWER_HEIGHT))    

            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col + ANSWER_WIDTH,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row + ANSWER_HEIGHT / 2))       

            pos.append((start_x + (ANSWER_WIDTH + ANSWER_GAP_X) * col + ANSWER_WIDTH - 50,
                start_y + (ANSWER_HEIGHT + ANSWER_GAP_Y) * row))            

            all_pos.append(pos)

    return all_pos
