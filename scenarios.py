"""
What my test runs. Unit 8, Milestone 3.

My five criteria (see criteria.md):
  1. false positives   -> "my own writing" (10 human pieces)
  2. score spread      -> "clear AI" (5) and "clear human" (5)
  3. label coverage    -> "label coverage" (one text for each label)
  4. appeal path       -> NOT here. Needs a submit then an appeal, so it lives in
                          extra_checks.py
  5. bad input         -> "bad input" bodies here, plus the non-JSON body and the
                          /ping + /health check in extra_checks.py (a dict body
                          can't say "this isn't JSON")

NOTE: the "my own writing" pieces are written in the style of my own plain
writing (emails, a school essay, notes). They were drafted with Claude's help
for the lab, so they are not scraped from my real files. I'm saying that here
so nobody thinks it's something it isn't.
"""

import csv
from pathlib import Path

HERE = Path(__file__).parent


def _attack_text(attack_id):
    """Grab one text out of the staff attack set so the label-coverage check uses a
    text that already got each label in the Milestone 2 run."""
    with open(HERE / "attack_set" / "attacks.csv", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["id"] == attack_id:
                return row["text"]
    raise KeyError(attack_id)


MY_WRITING = [
    # emails / notes / plain simple ones, not only the nice ones
    "hey, i cant make it to the group meeting thursday because my shift got moved. i read the notes you sent though. i think the survey part is the hardest so i can take that one if you want. just tell me what the deadline is and i will get it done before then",
    "My roommate left the dishes in the sink again. I did not say anything because I did not want a fight, but it has been three days. I think I am going to leave a note. Maybe a nice one. Maybe not that nice.",
    "Dear Professor, I am writing because I missed the quiz on Monday. I was sick and I have a note from the clinic. I know the syllabus says no makeups but I was hoping you could make an exception this one time. Thank you for your time.",
    "The bus was late again so I walked. It took forty minutes and my shoes got wet. By the time I got to class the door was already closed and I just stood in the hall for a minute. Then I went in anyway. Nobody really cared.",
    "I think the main thing I learned from this class is that I am bad at estimating how long things take. Every project I thought would take a weekend took two weeks. My plan for next semester is to double whatever number I come up with and then add a day.",
    "My grandma makes this soup that I have never been able to copy. I watched her do it twice. She does not measure anything. She just pours and tastes and says it needs more. I tried it at home and it tasted like hot water with carrots in it.",
    "For my essay I want to argue that school start times should be later. Teenagers do not get enough sleep, and I know that from my own life. When I get up at six I cannot think until lunch. Studies also say the same thing, which helps.",
    "We got to the lake around noon and the parking was full, so Dad dropped us off and went to find a spot. My sister and I put our towels down near the trees. The water was freezing but we went in anyway because we had already said we would.",
    "Quick update on the project: the login page works now but the signup page still breaks if you leave the email blank. I looked at it for an hour and I think the problem is in how I check the form. I will try again tomorrow after class.",
    "I do not really like writing about myself. Every time I start I just write what I think the teacher wants to read. So here is the honest version. I like cooking, I am bad at math, I have a dog named Biscuit, and I stay up too late.",
]

# 5 pieces I'm sure are AI (generated), and 5 I'm sure are human.
CLEAR_AI = [
    "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. Finally, it is essential to ensure that the system remains robust and scalable over time.",
    "Effective time management is a crucial skill that plays a significant role in both academic and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can maximize their productivity and achieve a healthy work-life balance. Furthermore, developing consistent habits contributes to long-term growth and overall well-being.",
    "Climate change represents one of the most pressing challenges facing our society today. It is essential to understand that its impacts are far-reaching, affecting ecosystems, economies, and communities around the world. Addressing this issue requires a coordinated effort across governments, industries, and individuals to promote sustainable practices and reduce emissions.",
    "In today's fast-paced digital landscape, the importance of cybersecurity cannot be overstated. Organizations must implement robust security measures to protect sensitive information from evolving threats. By fostering a culture of awareness and investing in the latest technologies, businesses can mitigate risks and ensure the continued trust of their stakeholders.",
    "Reading is a fundamental activity that offers numerous benefits for individuals of all ages. It enhances vocabulary, improves critical thinking skills, and provides valuable insights into different perspectives and cultures. Moreover, regular reading can reduce stress and foster a lifelong love of learning, making it an indispensable part of a well-rounded life.",
]
CLEAR_HUMAN = [
    "ok so the thing about my brother is he will eat literally anything if you dare him. last week it was a spoonful of mustard. mom walked in and just stared at us. he said it was fine. it was not fine, his eyes were watering for like ten minutes",
    "I lost my keys twice this week. The first time they were in the fridge, which I still cannot explain. The second time they were in my other jacket. My landlord says he will not make me a third copy so I bought a little bell thing to clip on them.",
    "Honestly the movie was fine. Not great. The ending dragged and the guy next to us kept checking his phone, which was annoying because the screen was so bright. I would watch it again on a plane maybe. Not at full ticket price though.",
    "Mr. Alvarez never once raised his voice in thirty years of teaching, and I only noticed after he retired. People brought it up at the party. Somebody said the quiet was scarier than yelling. I think that is true, I never wanted to disappoint him.",
    "We tried to fix the sink ourselves. Youtube made it look easy. Two hours and one flooded kitchen later we called a plumber, who laughed a little and then fixed it in ten minutes. It cost sixty dollars. Worth it, I think.",
]

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
    },
    {
        "name": "clear AI",
        "criterion": 2,
        "texts": CLEAR_AI,
    },
    {
        "name": "clear human",
        "criterion": 2,
        "texts": CLEAR_HUMAN,
    },
    {
        # One text per label. From the Milestone 2 run: EV05 got human, EV01 got
        # unsure, FP05 got ai. Order is human, unsure, ai.
        "name": "label coverage",
        "criterion": 3,
        "texts": [_attack_text("EV05"), _attack_text("EV01"), _attack_text("FP05")],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                       # no text field
            {"text": "", "creator_id": "eval_bad_empty"},             # empty
            {"text": "   ", "creator_id": "eval_bad_spaces"},         # whitespace
            {"text": 12345, "creator_id": "eval_bad_number"},         # number
            {"text": "word " * 20000, "creator_id": "eval_bad_huge"},  # 100,000 chars
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
