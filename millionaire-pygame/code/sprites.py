# thachlam's project
# remmeber to read the readme

from settings import * 
from os.path import join 

class Support:
    def __init__(self, support_type, index):
        self.display_surface = pygame.display.get_surface()
        self.support_type = support_type
        self.index = index

        self.start_x = WIDTH / 2 - (SUPPORT_WIDTH * 4 + SUPPORT_GAP * 3) / 2
        self.start_y = SUPPORT_START_Y
        self.rect = pygame.Rect(self.start_x + (SUPPORT_WIDTH + SUPPORT_GAP) * self.index, self.start_y,
                            SUPPORT_WIDTH, SUPPORT_HEIGHT)

        image = pygame.image.load(join("../images", str(support_type) + ".png"))
        x_image = pygame.image.load(join("../images", "unable.png"))
        
        self.image = pygame.transform.scale(image, (self.rect.width - 5, self.rect.height - 5))
        self.x_image = pygame.transform.scale(x_image, (self.rect.width - 5, self.rect.height - 5))

        self.used = False 
        self.checking = False
        self.activating = False

    def draw(self, question_set, question_rect, correct_answer):
        if self.checking:
            pygame.draw.rect(self.display_surface, "cyan", self.rect)

        x = self.rect.x + self.rect.width / 2 - self.image.get_width() / 2
        y = self.rect.y + self.rect.height / 2 - self.image.get_height() / 2
        
        self.display_surface.blit(self.image, (x, y))
        
        if self.used:
            self.display_surface.blit(self.x_image, (x, y))

        pygame.draw.rect(self.display_surface, "white", self.rect, 5)
        
        if self.activating:
            if self.support_type == "expert":
                answer = question_set["Answer"]
                hint = f"Choose {answer}! It's the best answer."
                text = FONT['answer'].render(hint, True, "white")
                self.display_surface.blit(text, (WIDTH / 2 - text.get_width() / 2, self.rect.bottom))
            
            elif self.support_type == "chart":
                if not self.option_percent:
                    self.calucalte_percent_activating_chart(correct_answer, question_set)

                for num, word in enumerate(["A", "B", "C", "D"]):
                    if word in question_set:
                        
                        text = FONT['answer'].render(word + ". " + str(self.option_percent[word]) + "%", True, "white")
                        x =  self.start_x + (SUPPORT_WIDTH + SUPPORT_GAP) * num
                        y = question_rect.bottom
                        
                        self.display_surface.blit(text, (x, y))                        


    def do_task(self, questions, question, task, pos):
        if self.support_type == "half":

            options = ["A", "B", "C", "D"]
            while len(options) != 2:
                option = random.choice(options)
                if option != questions[question]['Answer']:
                    options.remove(option)
                    del questions[question][option]


            # change the index if it was deleted
            if options[0] == "A":
                pos["col"], pos["row"] = 0, 0 
            elif options[0] == "B":
                pos["col"], pos["row"] = 1, 0
            elif options[0] == "C":
                pos["col"], pos["row"] = 0, 1


        elif self.support_type == "shuffle":
            task()

        elif self.support_type == "expert":
            self.activating = True
        else:
            self.activating = True
            self.option_percent = {}


    def calucalte_percent_activating_chart(self, correct_answer, question_set):
        total_percent = 0
        if correct_answer < 5:
            max_percent = 20 
        elif 5 <= correct_answer < 10:
            max_percent = 25 
        else:
            # the question is now hard so there is a case that audience can choose wrong answer
            max_percent = 27

        for word in ["A", "B", "C", "D"]:
            if word == question_set['Answer']:
                continue 
            else:
                if word in question_set:
                    percentage = random.randint(0, max_percent)
                    total_percent += percentage
                    self.option_percent[word] = percentage

        self.option_percent[question_set["Answer"]] = 100 - total_percent



class MoneyBoard:
    def __init__(self, font, money_level):
        self.font = font 
        self.money_level = money_level
        self.direction = "down"

        self.current_level = 0 
        self.width =  WIDTH 
        self.height = HEIGHT
        self.x = WIDTH / 2 - self.width / 2
        self.y = -self.height

        text = font.render("15. " + str(self.money_level[-1]), True, "black")
        _, _, self.rect_width, self.rect_height = text.get_rect()
        self.rect_width += 40
        self.rect_height -= 10

        self.screen = pygame.Surface((self.width, self.height))
        self.update_screen(-1)

        self.visible_timer = 0 
        self.visible_duration = 1.5
        self.answer_correctly = False 


    def display_boxes(self, text, text_color, box_color, x, y):
        pygame.draw.circle(self.screen, box_color, (x, y + self.rect_height / 2), self.rect_height / 2)
        pygame.draw.circle(self.screen, box_color, (x + self.rect_width, y + self.rect_height / 2), self.rect_height / 2)
        pygame.draw.rect(self.screen, box_color, (x, y, self.rect_width, self.rect_height))
        
        money_text = self.font.render(text, True, text_color)
        self.screen.blit(money_text, (self.width / 2 - money_text.get_width() / 2, y - 5))


    def update_screen(self, correct_answer):
        self.current_level = correct_answer + 2

        self.screen.fill("cyan")

        for i in range(len(self.money_level)):
            x = self.width / 2 - self.rect_width / 2
            y = i * 40

            if 15 - i < self.current_level:
                color = "green"
            elif 15 - i == self.current_level:
                color = "orange"
            else:
                color = "blue"

            text_color = "white" if i % 5 == 0 else "black"
            money_to_string = MONEY_IN_STRING[self.money_level[-(i + 1)]]
            text = f"{15 - i}. {money_to_string}"
            self.display_boxes(text, text_color, color, x, y + 5)

            
    def move(self):
        if self.y < 0 and self.direction == "down":
            self.y += 5
        else:
            if not self.visible_timer:
                self.visible_timer = time.time()

        if (self.direction == "down" 
            and time.time() - self.visible_timer >= self.visible_duration\
            and self.answer_correctly and self.visible_timer):
            self.direction = "up"
            self.answer_correctly = False


        elif self.y > -self.height and self.direction == "up":
            self.y -= 5