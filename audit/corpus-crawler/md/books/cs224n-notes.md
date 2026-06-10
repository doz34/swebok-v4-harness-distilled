<script src="header.js"></script> - We just replicate navbar and header in pages as faster and better with search engines
Navbar
Header
Intro
<p>
  <font style="color: #8c1515; font-weight: bold">Note: In the 2023–24
  academic year, CS224N will be taught in both Winter and
  Spring 2024.</font>
  </p>

Natural language processing (NLP) is a crucial part of artificial intelligence (AI), modeling how people share information. In recent years, deep learning approaches have obtained very high performance on many NLP tasks. In this course, students gain a thorough introduction to cutting-edge neural networks for NLP.
Staff Info
<div class="row">

### Instructors

Diyi Yang

Yejin Choi

### Course Staff

John Cho (Course Manager)

Swati Dube Batra (Course Manager Advisor)

### Teaching Assistants

Julie Kallini (Head TA)

Ahmed Ahmed

David Anugraha

Luke Bailey

Sarah Chen

Caroline Choi

Advit Deepak

Nevin George

Simon Kim

Ali Sartaz Khan

Arpandeep Khatua

Alisa Levin

Shicheng Liu

Wei Liu

Minsik Oh

Chenglei Si

Mirac Suzgun

Tristan Thrush

Fang Wu

Qinan Yu
Logistics

## Logistics

- **Lectures:** are on Tuesday/Thursday 4:30 PM - 5:50 PM Pacific Time in [NVIDIA Auditorium](https://goo.gl/maps/hRjQYd6MqxB2). The lectures will also be livestreamed on [Canvas](https://canvas.stanford.edu/) via Panopto.
- **Lecture videos for enrolled students:** are posted on [Canvas](https://canvas.stanford.edu/courses/217005/external_tools/69960) (requires login) shortly after each lecture ends. Unfortunately, it is not possible to make these videos viewable by non-enrolled students.
- **Publicly available lecture videos and versions of the course:** Complete videos for the CS224N course are available (free!) on [the CS224N 2024 YouTube playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D). Anyone is welcome to enroll in [XCS224N: Natural Language Processing with Deep Learning](https://online.stanford.edu/courses/xcs224n-natural-language-processing-deep-learning), the Stanford Artificial Intelligence Professional Program version of this course, throughout the year (medium fee, community TAs and certificate). Stanford students enroll normally in CS224N and others can also enroll in [CS224N via Stanford online](https://online.stanford.edu/courses/cs224n-natural-language-processing-deep-learning) (high cost, limited enrollment, gives Stanford credit). The lecture slides and assignments are updated online each year as the course progresses. We are happy for anyone to use these resources, and we are happy to get acknowledgements.
- **Office hours**: Hybrid format with remote (over Zoom) or in person options. Information [here](office_hours.html).
- **Contact**: Students should ask *all* course-related questions in the Ed forum, where you will also find announcements. You will find the course Ed on the course Canvas page or in the header link above. For external enquiries, emergencies, or personal matters that you don't wish to put in a private Ed post, you can email us at *cs224n-staff-win2526@cs.stanford.edu*. Please send all emails to this mailing list - do not email the instructors directly.
Content

## Content

### What is this course about?

Natural language processing (NLP) or computational linguistics is one of the most important technologies of the information age. Applications of NLP are everywhere because people communicate almost everything in language: web search, advertising, emails, customer service, language translation, virtual agents, medical reports, politics, etc. In the 2010s, deep learning (or neural network) approaches obtained very high performance across many different NLP tasks, using single end-to-end neural models that did not require traditional, task-specific feature engineering. In the 2020s amazing further progress was made through the scaling of Large Language Models, such as ChatGPT. In this course, students will gain a thorough introduction to both the basics of Deep Learning for NLP and the latest cutting-edge research on Large Language Models (LLMs). Through lectures, assignments and a final project, students will learn the necessary skills to design, implement, and understand their own neural network models, using the [Pytorch](https://pytorch.org/) framework.

> “Take it. CS221 taught me algorithms. CS229 taught me math. CS224N taught me how to write machine learning models.”
> – A CS224N student on Carta

### Previous offerings

Below you can find archived websites and student project reports from previous years. **Disclaimer: assignments change from year to year; please do not do assignments from previous years!**
| **CS224N Websites**: [Winter 2025](https://web.stanford.edu/class/archive/cs/cs2 |
| -------------------------------------------------------------------------------- |
| **CS224N Lecture Videos**: [Spring 2024](https://www.youtube.com/playlist?list=P |
| **CS224N Reports**: [Winter 2024](https://web.stanford.edu/class/archive/cs/cs22 |
| **CS224d Reports**: [Spring 2016](http://cs224d.stanford.edu/reports_2016.html)  |

### Prerequisites

- **Proficiency in Python** All class assignments will be in Python (using [NumPy](https://numpy.org/) and [PyTorch](https://pytorch.org)). If you need to remind yourself of Python, or you're not very familiar with NumPy, you can come to the Python review session in week 1 (listed in the schedule). If you have a lot of programming experience but in a different language (e.g. C/C++/Matlab/Java/Javascript), you will probably be fine.
- **College Calculus, Linear Algebra** (e.g. MATH 51, CME 100) You should be comfortable taking (multivariable) derivatives and understanding matrix/vector notation and operations.
- **Basic Probability and Statistics** (e.g. CS 109 or equivalent) You should know the basics of probabilities, gaussian distributions, mean, standard deviation, etc.
- **Foundations of Machine Learning** (e.g. CS221, CS229, CS230, or CS124) We will be formulating cost functions, taking derivatives and performing optimization with gradient descent. If you already have basic machine learning and/or deep learning knowledge, the course will be easier; however it is possible to take CS224N without it. There are many introductions to ML, in webpage, book, and video form. One approachable introduction is Hal Daumé’s in-progress [*A Course in Machine Learning*](https://web.archive.org/web/20250114002202/http://ciml.info/dl/v0_99/ciml-v0_99-all.pdf). Reading the first 5 chapters of that book would be good background. Knowing the first 7 chapters would be even better!

### Reference Texts

The following texts are useful, but none are required. All of them can be read free online.

- Dan Jurafsky and James H. Martin. [Speech and Language Processing (2024 pre-release)](https://web.stanford.edu/~jurafsky/slp3/)
- Jacob Eisenstein. [Natural Language Processing](https://github.com/jacobeisenstein/gt-nlp-class/blob/master/notes/eisenstein-nlp-notes.pdf)
- Yoav Goldberg. [A Primer on Neural Network Models for Natural Language Processing](http://u.cs.biu.ac.il/~yogo/nnlp.pdf)
- Ian Goodfellow, Yoshua Bengio, and Aaron Courville. [Deep Learning](http://www.deeplearningbook.org/)
- Delip Rao and Brian McMahan. [Natural Language Processing with PyTorch](https://searchworks.stanford.edu/view/13241676) (requires Stanford login).
- Lewis Tunstall, Leandro von Werra, and Thomas Wolf. [Natural Language Processing with Transformers](https://transformersbook.com/)

If you have no background in neural networks but would like to take the course anyway, you might well find one of these books helpful to give you more background:

- Michael A. Nielsen. [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com)
- Eugene Charniak. [Introduction to Deep Learning](https://mitpress.mit.edu/books/introduction-deep-learning)
Coursework
Note the margin-top:-20px and the <br> serve to make the #coursework hyperlink display correctly (with the h2 header visible)

## Coursework
Disclaimer: Coursework is tentative and subject to change!

### Assignments (48%)

There are four weekly assignments, which will improve both your theoretical understanding and your practical skills. All assignments contain both written questions and programming parts. In office hours, TAs may look at students’ code for assignments 1 and 2, but not for assignments 3 and 4.

- **Credit**: Assignment 1 (6%): Introduction to word vectors Assignment 2 (14%): Neural network foundations, calculating tensor derivatives, dependency parsing Assignment 3 (14%): Self-attention and Transformers Assignment 4 (14%): Large language model benchmarking and evaluation
- **Deadlines**: All assignments are due on either a Tuesday or a Thursday *before class* (i.e. before 4:30pm). All deadlines are listed in the schedule.
- **Submission**: Assignments are submitted via [Gradescope](https://www.gradescope.com/courses/1208404). You will be able to access the course Gradescope page on Canvas. If you need to sign up for a Gradescope account, please use your @stanford.edu email address. Further instructions are given in each assignment handout. *Do not email us your assignments*.
- **Late start**: If the result gives you a higher grade, we will not use your assignment 1 score, and we will give you an assignment grade based on counting each of assignments 2–4 at 16%.
- **Collaboration**: Study groups are allowed, but students must understand and complete their own assignments, and hand in one assignment per student. If you worked in a group, please put the names of the members of your study group at the top of your assignment. Please ask if you have any questions about the collaboration policy.
- **Honor Code**: We expect students to not look at solutions or implementations online. Like all other classes at Stanford, we take the student [Honor Code](https://ed.stanford.edu/academics/masters-handbook/honor-code) seriously. We sometimes use automated methods to detect overly similar assignment solutions.

### Final Project (49%)

The Final Project offers you the chance to apply your newly acquired skills towards an in-depth application. Students have two options: the **Default Final Project** (in which students tackle a predefined task, namely implementing a minimalist version of GPT-2) or a **Custom Final Project** (in which students choose their own project involving human language and deep learning). Examples of both can be seen on the [Spring 2024 website](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/project.html). *Note: TAs may not look at students' code for either the default or custom final projects. The Spring 2024 Default Final Project was based on BERT and has now been replaced with GPT-2.*

#### Important information

- **Credit**: For both default and custom projects, credit for the final project is broken down as follows: Project proposal (8%) Project milestone (6%) Project poster (3%) Project report (32%)
- **Deadlines**: The project proposal, milestone and report are all due at 4:30pm. All deadlines are listed in the schedule.
- **Default Final Project**: In this project, students implement parts of the GPT-2 architecture and use it to tackle 3 downstream tasks. Similar to previous years, the code is in PyTorch.
- **Project advice** [[lecture slides](slides_w26/cs224n-2026-lecture06-final-project.pdf)] [[custom project tips](project/custom-final-project-tips.pdf)]: The *Practical Tips for Final Projects* lecture provides guidance for choosing and planning your project. To get project advice from staff members, first look at each staff member's areas of expertise on the [office hours page](office_hours.html#staff). This should help you find a staff member who is knowledgable about your project area.
- **Ethics-related questions**: For guidance on projects dealing with ethical questions, or ethical questions that arise during your project, please contact Wanheng Hu (*wanhenghu@stanford.edu*) or Justin Shin (*justinjs@stanford.edu*).

#### Practicalities

- **Team size**: Students may do final projects solo, or in teams of up to 3 people. We strongly recommend you do the final project in a team. Larger teams are expected to do correspondingly larger projects, and you should only form a 3-person team if you are planning to do an ambitious project where every team member will have a significant contribution.
- **Contribution**: In the final report we ask for a statement of what each team member contributed to the project. Team members will typically get the same grade, but we may differentiate in extreme cases of unequal contribution. You can contact us in confidence in the event of unequal contribution.
- **External collaborators**: You can work on a project that has external (non CS224N student) collaborators, but you must make it clear in your final report which parts of the project were your work.
- **Sharing projects**: You can share a single project between CS224N and another class, but we expect the project to be accordingly bigger, and you must declare that you are sharing the project in your project proposal.
- **Mentors**: Every custom project team has a mentor, who gives feedback and advice during the project. Default project teams do not have mentors. A project may have an external (i.e., not course staff) mentor; otherwise, we will assign a CS224N staff mentor to custom project teams after project proposals.
- **Computing resources**: All teams will receive compute credits thanks to kind donations by Google, Kimi, Modal, and Qwen!
- **Using external resources**: The following guidelines apply to all projects (though the default project has some more specific rules, details provided in the *Honor Code* section of the [handout](project_w25/CS_224n__Default_Final_Project__Build_GPT_2.pdf)): You can use any deep learning framework you like (PyTorch, TensorFlow, etc.) More generally, you may use any existing code, libraries, etc. and consult any papers, books, online references, etc. for your project. However, you must cite your sources in your writeup and clearly indicate which parts of the project are your contribution and which parts were implemented by others. Under no circumstances may you look at another CS224N group's code, or incorporate their code into your project.

### Participation (3%)

We appreciate everyone being actively involved in the class! There are several ways of earning participation credit, which is capped at 3%:

- **Attending guest speakers' lectures**:
- **Completing feedback surveys**: We will send out two feedback surveys (mid-quarter and end-of-quarter) to help us understand how the course is going, and how we can improve. Each of the two surveys are worth 0.5%.
- **Ed participation**: The top ~20 contributors to Ed will get 3%; others will get credit in proportion to the participation of the ~20th person.
- **Karma point**: Any other act that improves the class, like helping out another student in office hours or writing a useful guide for students on some topic, which a CS224N TA or instructor notices and deems worthy: 1%
<h3>Late Days</h3>
  <ul>
    <li>Each student has 6 late days to use. A late day extends the deadline 24 hours. You can use up to 3 late days per assignment (including all four assignments, project proposal, project milestone and project final report).</li>
    <li>Final project teams can <b>share</b> late days between members. For example, a group of three people must have at least six late days between them to extend the deadline by two days. <em>If any late days are being shared, this must be clearly marked at the beginning of the report, and we will release a form on Ed that teams should fill out.</em>.</li>
    <li>Once you have used all 6 late days, the penalty is 1% off the final course grade for each additional late day.</li>
  </ul>

### Late Days

- Each student has 6 late days to use. A late day extends the deadline 24 hours. You can use up to 3 late days per assignment (including all four assignments, project proposal, project milestone, and project final report).
- Once you have used all 6 late days, the penalty is 1% off the final course grade for each additional late day.
- **Project proposal and milestone (late days are NOT shared):** Late days are applied individually and are not pooled across the team. If a student does not have enough late days remaining, that student receives a 1% deduction to their total course grade for each late day they are short — this penalty applies only to that student.
- **Final project report (late days CAN be shared):** Late days may be pooled across team members. For example, in a team of three students, the team's total available late days is the sum of each member's remaining late days, divided by three to determine how many days late the team can submit. *At the top of your final report, you must state how many late days your team is pooling and which team members have late days remaining.*

### Regrade Requests

If you feel you deserved a better grade on an assignment, you may submit a regrade request on Gradescope within 3 days after the grades are released. Your request should briefly summarize why you feel the original grade was unfair. Your TA will reevaluate your assignment as soon as possible, and then issue a decision. If you are still not happy, you can ask for your assignment to be regraded by an instructor. **Disclaimer: the course staff reserve the right to regrade your entire assignment in addition to the specific questions you request. Submit regrade requests at your own risk.**

### Credit/No credit enrollment

If you take the class credit/no credit then you are graded in the same way as those registered for a letter grade. The only difference is that, providing you reach a C- standard in your work, it will simply be graded as CR.

### All students welcome

We are committed to doing what we can to work for equity and to create an inclusive learning environment that actively values the diversity of backgrounds, identities, and experiences of everyone in CS224N. We also know that we will sometimes make missteps. If you notice some way that we could do better, we hope that you will let someone in the course staff know about it.

### Well-Being and Mental Health

If you are experiencing personal, academic, or relationship problems and would like to talk to someone with training and experience, reach out to the [Counseling and Psychological Services (CAPS)](https://vaden.stanford.edu/caps-and-wellness) on campus. CAPS is the university’s counseling center dedicated to student mental health and wellbeing. Phone assessment appointments can be made at CAPS by calling 650-723-3785, or by accessing the VadenPatient portal through the Vaden website.

### Auditing the course

In general we are happy to have auditors if they are a member of the Stanford community (registered student, official visitor, staff, or faculty). If you are interested, email us at *cs224n-staff-win2526@cs.stanford.edu*. If you want to actually master the material of the class, we very strongly recommend that auditors do all the assignments. However, due to high enrollment, we cannot grade the work of any students who are not officially enrolled in the class.

### Students with Documented Disabilities

We assume that all of us learn in different ways, and that the organization of the course must accommodate each student differently. We are committed to ensuring the full participation of all enrolled students in this class. If you need an academic accommodation based on a disability, you should initiate the request with the [Office of Accessible Education (OAE)](https://oae.stanford.edu/). The OAE will evaluate the request, recommend accommodations, and prepare a letter for faculty. Students should contact the OAE as soon as possible and at any rate in advance of assignment deadlines, since timely notice is needed to coordinate accommodations. Students should also send your accommodation letter to either the staff mailing list (*cs224n-staff-win2526@cs.stanford.edu*) or make a private post on Ed, as soon as possible.

**OAE accommodations for group projects:** OAE accommodations will not be extended to collaborative assignments.

### AI Tools Policy

Students are required to independently submit their solutions for CS224N homework assignments. Collaboration with generative AI tools such as Co-Pilot and ChatGPT is allowed, treating them as collaborators in the problem-solving process. However, the direct solicitation of answers or copying solutions, whether from peers or external sources, is strictly prohibited.

**Employing AI tools to substantially complete assignments or exams will be considered a violation of the Honor Code.** For additional details, please refer to the Generative AI Policy Guidance [here](https://communitystandards.stanford.edu/generative-ai-policy-guidance).

### Sexual violence

Academic accommodations are available for students who have experienced or are recovering from sexual violence. If you would like to talk to a confidential resource, you can schedule a meeting with the Confidential Support Team or call their 24/7 hotline at: 650-725-9955. Counseling and Psychological Services also offers confidential counseling services. Non-confidential resources include the Title IX Office, for investigation and accommodations, and the SARA Office, for healing programs. Students can also speak directly with the teaching staff to arrange accommodations. Note that university employees – including professors and TAs – are required to report what they know about incidents of sexual or relationship violence, stalking and sexual harassment to the Title IX Office. Students can learn more at [https://vaden.stanford.edu/sexual-assault](are recovering from).
Schedule
Note the margin-top:-20px and the <br> serve to make the #schedule hyperlink display correctly (with the h2 header visible)

## Schedule

Updated lecture **slides** will be posted here shortly before each lecture. Lecture **notes** will be uploaded a few days after most lectures. The notes (which cover approximately the first half of the course content) give supplementary detail beyond the lectures.

**Disclaimer: Schedule is tentative and subject to change!** **Disclaimer: Assignments change; please do not do old assignments. We will give no points for doing last year's assignments.**
| Date                                                                             | Description                                                                      | Course Materials                                                                 | Events                                                                           | Deadlines                                                                        |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Week 1** Tue Jan 6                                                             | History of NLP [[intro slides](slides_w26/cs224n-2026-lecture01-intro.pdf)] [[hi | Suggested Readings: [Human Language Understanding & Reasoning](https://www.amaca | Assignment 1 **out** [[code](assignments_w26/a1.zip)]                            |                                                                                  |
| Thu Jan 8                                                                        | Word Vectors [[slides](slides_w26/cs224n-2026-lecture02-wordvecs.pdf)] [[notes 1 | Suggested Readings: [Efficient Estimation of Word Representations in Vector Spac |                                                                                  |                                                                                  |
| Fri Jan 9                                                                        | Python Review Session [[slides](slides_w25/2024 CS224N Python Review Session Sli | ** Time 1:30pm-2:50pm Location NVIDIA Auditorium                                 |                                                                                  |                                                                                  |
| **Week 2** Tue Jan 13                                                            | Backpropagation and Neural Network Basics [[slides](slides_w26/cs224n-2026-lectu | Suggested Readings: [matrix calculus notes](readings/gradient-notes.pdf) [Review | Assignment 2 **out** [[code](assignments_w26/a2.zip)] [[handout](assignments_w26 | Assignment 1 **due**                                                             |
| Thu Jan 15                                                                       | Language Models and RNNs [[slides](slides_w26/cs224n-2026-lecture04-rnnlm.pdf)]  | Suggested Readings: [Learning long-term dependencies with gradient descent is di |                                                                                  |                                                                                  |
| Fri Jan 16                                                                       | PyTorch Tutorial Session [[colab](https://colab.research.google.com/drive/1Pz8b_ | ** Time 1:30pm-2:50pm Location NVIDIA Auditorium                                 |                                                                                  |                                                                                  |
| **Week 3** Tue Jan 20                                                            | Transformers [[slides](slides_w26/cs224n-2026-lecture05-transformers.pdf)] [[not | Suggested Readings: [Attention Is All You Need](https://arxiv.org/abs/1706.03762 |
| Thu Jan 22                                                                       | Final Projects: Custom and Default; Practical Tips [[slides](slides_w26/cs224n-2 | Suggested Readings: [Practical Methodology](https://www.deeplearningbook.org/con | Assignment 3 **out** [[code](assignments_w26/a3.zip)] [[handout](assignments_w26 | Assignment 2 **due**                                                             |
| **Week 4** Tue Jan 27                                                            | Pretraining (Scaling, Systems, Data) [[slides](slides_w26/cs224n-2026-lecture07- | Suggested Readings: [BERT: Pre-training of Deep Bidirectional Transformers for L |                                                                                  |                                                                                  |
| Thu Jan 29                                                                       | Post-training (RLHF, SFT, DPO) [[slides](slides_w26/cs224n-2026-lecture08-posttr | Suggested Readings: [Aligning language models to follow instructions](https://op | Project Proposal **out** [[handout](project/Project_Proposal_Instructions.pdf)]  |                                                                                  |
| **Week 5** Tue Feb 3                                                             | Efficient Adaptation (Prompting + PEFT) [[slides](slides_w26/cs224n-2026-lecture | Suggested Readings: [Language Models are Few-Shot Learners](https://arxiv.org/ab |                                                                                  |                                                                                  |
| Thu Feb 5                                                                        | Agents, Tool Use, and RAG [[slides](slides_w26/cs224n-2026-lecture10-rag-agents. | Suggested Readings: [ReAct: Synergizing Reasoning and Acting in Language Models] | Assignment 4 **out** [[code](assignments_w26/a4.zip)] [[handout](assignments_w26 | Assignment 3 **due**                                                             |
| Fri Feb 6                                                                        | Hugging Face Transformers Tutorial Session [[slides](materials/hf_transformers_t | **Time 1:30pm-2:50pm Location NVIDIA Auditorium                                  |                                                                                  |                                                                                  |
| **Week 6** Tue Feb 10                                                            | Benchmarking and Evaluation [[slides](slides_w26/cs224n-2026-lecture11-evaluatio | Suggested Readings: [Challenges and Opportunities in NLP Benchmarking](https://w |                                                                                  | Project Proposal & Mentor Form **due**                                           |
| Thu Feb 12                                                                       | Reasoning 1 [[slides](slides_w26/cs224n-2026-lecture12-reasoning-part1.pdf)]     | Suggested Readings: [Chain-of-Thought Prompting Elicits Reasoning in Large Langu |                                                                                  |                                                                                  |
| **Week 7** Tue Feb 17                                                            | Reasoning 2 [[slides](slides_w26/cs224n-2026-lecture13-reasoning-part2.pdf)]     | Suggested Readings: [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050 | Project Milestone **out** [[handout](project/Project_Milestone_Instructions.pdf) | Final Project Proposals **returned**                                             |
| Thu Feb 19                                                                       | Guest Lecture: Tokenization and Multilinguality (by [Julie Kallini](https://juli | Suggested readings: [Jurafsky & Martin Chapter 2](https://web.stanford.edu/~jura |                                                                                  | Assignment 4 **due**                                                             |
| **Week 8** Tue Feb 24                                                            | Guest Lecture: Interpretability (by [Been Kim](https://beenkim.github.io/)) <br> | Suggested readings: [Because we have LLMs, we Can and Should Pursue Agentic Inte | Final Project Report Instructions **out** [[Instructions](project/Project_Report |                                                                                  |
| Thu Feb 26                                                                       | Social and Broader Impacts of NLP (Risks) [[slides](slides_w26/cs224n-2026-lectu |                                                                                  |                                                                                  | Final Project Milestone **due**                                                  |
| Fri Feb 27                                                                       |                                                                                  |                                                                                  |                                                                                  | **Course Withdrawal Deadline**                                                   |
| **Week 9** Tue Mar 3                                                             | Guest Lecture: Multimodality (by [Luke Zettlemoyer](https://homes.cs.washington. | Suggested readings: [Visual Sketchpad: Sketching as a Visual Chain of Thought fo |                                                                                  | Final Project Milestones **returned**                                            |
| Thu Mar 5                                                                        | Guest Lecture: Tinker and LoRA Without Regret (by [John Schulman](http://joschu. |                                                                                  |                                                                                  |
| **Week 10** Tue Mar 10                                                           | Open Questions in NLP 2026 [[slides](slides_w26/cs224n-2026-lecture19-open-quest |                                                                                  |                                                                                  |                                                                                  |
| Thu Mar 12                                                                       | No Lecture                                                                       |                                                                                  |                                                                                  | Final project **due**                                                            |
| Mon Mar 16                                                                       | Final Project Poster Session <br> [<a href="readings/cs224n-python-review-code-u | ** Time 12:15pm-3:15pm Location AOERC , Time 12:15pm-3:15pm [<a href="project.ht |                                                                                  | [[Printing guide](https://docs.google.com/document/d/1J8-TVVvndimSwq3jGzpMO_OtPA |
Sponsors

## Sponsors

We are grateful to our sponsors for their generous support of CS224N.

jQuery and Bootstrap