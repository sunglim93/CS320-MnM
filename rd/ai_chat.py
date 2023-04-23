import openai

<<<<<<< Updated upstream
openai.api_key = ""
=======
openai.api_key = "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"
>>>>>>> Stashed changes
#insert API key here

class NPC:
    def __init__(self, name, prompt):
        self.name = name
        self.dialogue = ""
        completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.9,
        )
        message = completions.choices[0].text
        self.message = message.strip()

while True:
    player_prompt = input("Player: ")
    if player_prompt == "exit":
        break
    else:
        with open("corpus.txt", "r") as corpus_file:
            corpus_text = corpus_file.read()
            final_input = player_prompt
        npc = NPC("Gus: ", final_input)
        print(npc.name + npc.message)
