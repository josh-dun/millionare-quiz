# thachlam's project
# remmeber to read the readme

from settings import *
from sprites import * 
from word_list import * 
from support import *
from copy import deepcopy 

pygame.init()

class Game:
    def __init__(self):        
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Who wants to be a millionaire?")
        # tools
        self.logic_tools = LogicTools()
        self.draw_tools = drawTools(self.logic_tools)

        # answer
        self.answers = ["A", "B", "C", "D"]
        self.answer_boxes = get_answer_polygon_pos()
        self.money_level = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

        self.shortcut_visible = True
        self.level = ""
        self.resetGame()


    def resetGame(self):
        # set question
        self.all_questions = deepcopy(EASY)
        self.question = ""

        # setup answer
        self.correct_answer = 0
        self.answer_index = {'row': 0, 'col': 0}
        
        # setup money
        self.money_board = MoneyBoard(FONT['money'], self.money_level)
        self.current_money = 100
        self.money_visible = False 

        # support
        support_type = ["half", "expert", "chart", "shuffle"]
        self.supports = [Support(support_type[i], i) for i in range(len(support_type))]
        self.active_support = False 
        self.support_index = 0
        self.amount_current_support = 4

        # timer 
        self.leak_answer_timer = 0 
        self.answer_duration = 1

        # state
        self.state = "continue"

    def shuffle_options(self):
        self.question_set = self.all_questions[self.question]
        for word in ["A", "B", "C", "D"]:
            option = random.choice(self.question_set['Options'])
            self.question_set[word] = option 
            self.question_set['Options'].remove(option)

            if option == self.question_set['Answer']:
                self.question_set['Answer'] = word

        del self.question_set['Options']

    def show_answer(self):
        if time.time() - self.leak_answer_timer <= self.answer_duration:
            index = self.answer_index['col'] + self.answer_index['row'] * 2     
            
            # fill the answer box with the color red
            if self.answers[index] != self.all_questions[self.question]['Answer']:                
                self.update_answer_box(index, "red")

            # fill the answer box with the color green
            num = self.answers.index(self.all_questions[self.question]['Answer'])
            self.update_answer_box(num, "green")

        # after update the animation, update question and give player a point
        else:
            self.correct_answer += 1
            if self.correct_answer <= len(self.money_level) - 1:
                self.current_money = self.money_level[self.correct_answer]

            if self.correct_answer == 5 or self.correct_answer == 10:
                self.level = "change"

            self.change_question()

            if self.correct_answer == 15:
                self.state = "win"


    def draw_window(self):
        self.win.fill("black")
            
        self.draw_tools.display_instructions(self.shortcut_visible, self.current_money, self.correct_answer)

        if not self.question:
            self.question = random.choice(list(self.all_questions.keys()))
            self.shuffle_options()


        question_rect = self.draw_tools.draw_question_bar()
        self.draw_tools.display_long_text('question', str(self.correct_answer + 1) + ". " + self.question, question_rect, 45)
        

        for num, pos in enumerate(self.answer_boxes):
            if self.answer_index['col'] + self.answer_index['row'] * 2 == num and not self.active_support:
                color = "orange"
            else:
                color = "white"

            if self.answers[num] in self.all_questions[self.question]:
                self.update_answer_box(num, color)
 
        if self.leak_answer_timer:
            self.show_answer()

        # draw the support boxes
        for support in self.supports:
            support.draw(self.question_set, question_rect, self.correct_answer)
            support.checking = True if (support.index == self.support_index and self.active_support) else False

        # draw the money board
        if self.money_visible:
            self.win.blit(self.money_board.screen, (self.money_board.x, self.money_board.y))

        # draw if lose or win
        if self.state != "continue" and not self.leak_answer_timer:
            self.draw_tools.draw_end_game_with_state(self.state, self.leak_answer_timer, self.current_money, self.resetGame)
              

    def check_answer(self):
        num = self.answer_index['col'] + self.answer_index['row'] * 2
        self.all_questions[self.question]['Answer']
        if ANSWERS[num] == self.all_questions[self.question]['Answer']:
            self.money_board.update_screen(self.correct_answer)
            return "continue"
        else:
            return "lose"

    def change_question(self):      
        if self.correct_answer == 5 and self.level == "change":
            self.all_questions = deepcopy(MEDIUM)
            self.level = ""
        elif self.correct_answer == 10 and self.level == "change":
            self.all_questions = deepcopy(HARD)
            self.level = ""

        else:
            del self.all_questions[self.question]

            
        self.question = random.choice(list(self.all_questions.keys()))

        self.shuffle_options()
        self.leak_answer_timer = 0
        self.answer_index = {'row': 0, 'col': 0}

        for support in self.supports:
            if support.activating:
                support.activating = False

    
    def update_answer_box(self, index, color):
        box = self.answer_boxes[index]
        pygame.draw.polygon(self.win, color, box)
        
        rect = pygame.Rect(box[0][0], box[0][1], ANSWER_WIDTH - 100, ANSWER_HEIGHT)
        answer = self.answers[index] + ". " + self.all_questions[self.question][self.answers[index]]
        
        self.draw_tools.display_long_text('answer', answer, rect, 20)


    def run(self):
        run = True 

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h and not self.money_visible:
                        if not self.active_support and self.amount_current_support > 0:
                            self.active_support = True
                            for support in self.supports:
                                if not support.used: 
                                    self.support_index = support.index 
                                    break

                        else:
                            self.active_support = False


                    if event.key == pygame.K_m and not self.money_board.answer_correctly:
                        if not self.money_visible:
                            self.money_visible = True

                        if self.money_board.direction == "down":
                            self.money_board.direction = "up"

                        else:
                            self.money_board.direction = "down"

                    if not self.money_visible:
                        if event.key == pygame.K_RIGHT:
                            if not self.active_support:
                                self.logic_tools.get_answer_index(self.answer_index, 1, 0, self.question_set)            
                            else:
                                self.support_index = self.logic_tools.get_support_index(self.support_index, self.supports, 1)

                        if event.key == pygame.K_LEFT:
                            if not self.active_support:
                                self.logic_tools.get_answer_index(self.answer_index, -1, 0, self.question_set)
                            else:
                                self.support_index = self.logic_tools.get_support_index(self.support_index, self.supports, -1)

                        if event.key == pygame.K_DOWN:
                            if not self.active_support:
                                self.logic_tools.get_answer_index(self.answer_index, 0, 1, self.question_set)

                        if event.key == pygame.K_UP:
                            if not self.active_support:
                                self.logic_tools.get_answer_index(self.answer_index, 0, -1, self.question_set)
                            
                        if event.key == pygame.K_SPACE and self.state == "continue":
                            if self.active_support == False:
                                self.state = self.check_answer()
                                self.leak_answer_timer = time.time()
                                
                                if self.state == "continue":
                                    self.money_board.answer_correctly = True 
                                    self.money_visible = True 
                                    self.money_board.direction = "down"


                            else:
                                self.supports[self.support_index].used = True 
                                self.supports[self.support_index].do_task(self.all_questions, self.question, self.change_question, self.answer_index)
                                self.active_support = False
                                self.amount_current_support -= 1

                    if event.key == pygame.K_t:
                        self.state = "take-money"


                    if event.key == pygame.K_s:
                        if self.shortcut_visible:
                            self.shortcut_visible = False
                        else:
                            self.shortcut_visible = True
                    

            self.draw_window()
            
            
            if self.money_visible:
                self.money_board.move()
                if self.money_board.direction == "up" and self.money_board.y <= -self.money_board.height:
                    self.money_visible = False
                    self.money_board.visible_timer = 0

            pygame.display.update()


        pygame.quit()
        quit()


game = Game()
game.run()