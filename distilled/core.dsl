# SWEBOK v4 Distilled — Core Principles DSL
# Compiled from 872 reference works. Each principle has a citation density
# (number of books that independently endorse the principle).
#
# Format: PRINCIPLE: NAME ;; DOMAIN ;; CITATION_DENSITY ;; SYNTHESIS
# Density: HIGH (>50 books), MEDIUM (10-50), LOW (1-10)

PRINCIPLE: KISS ;; all-domains ;; HIGH:>100
SYNTHESIS: "Keep It Simple, Stupid. Prefer simple solutions. Complexity is the
root of all software evil. Simplicity is the ultimate sophistication."

PRINCIPLE: YAGNI ;; all-domains ;; HIGH:>80
SYNTHESIS: "You Aren't Gonna Need It. Don't add functionality until it is
necessary. Speculative features become maintenance burden."

PRINCIPLE: DRY ;; all-domains ;; HIGH:>100
SYNTHESIS: "Don't Repeat Yourself. Every piece of knowledge must have a single,
unambiguous, authoritative representation within a system."

PRINCIPLE: SOLID ;; software-engineering ;; HIGH:>100
SYNTHESIS: "SRP (Single Responsibility), OCP (Open/Closed), LSP (Liskov
Substitution), ISP (Interface Segregation), DIP (Dependency Inversion)."

PRINCIPLE: SLAP ;; software-engineering ;; MEDIUM:30
SYNTHESIS: "Single Level of Abstraction Principle. All statements in a
function should belong to the same level of abstraction."

PRINCIPLE: SEPARATION_OF_CONCERNS ;; software-engineering ;; HIGH:>100
SYNTHESIS: "Different concerns belong in different modules. Coupling should
be low. Cohesion should be high."

PRINCIPLE: PRINCIPLE_OF_LEAST_ASTONISHMENT ;; software-engineering ;; MEDIUM:40
SYNTHESIS: "A component should behave as its users would expect. Surprise
is the enemy of trust."

PRINCIPLE: POSTELS_LAW ;; software-engineering ;; MEDIUM:25
SYNTHESIS: "Be conservative in what you send, liberal in what you accept.
(Forgiving input, strict output.)"

PRINCIPLE: BOY_SCOUT_RULE ;; software-engineering ;; MEDIUM:20
SYNTHESIS: "Leave the campground cleaner than you found it. Every commit
should make the code a little better than before."

PRINCIPLE: RULE_OF_THREE ;; software-engineering ;; HIGH:>50
SYNTHESIS: "Wait until you've written the same thing three times before
abstracting. Two instances is coincidence, three is a pattern."

PRINCIPLE: CONWAYS_LAW ;; software-engineering ;; HIGH:>60
SYNTHESIS: "Organizations which design systems are constrained to produce
designs which are copies of the communication structures of these organizations."

PRINCIPLE: HICHS_LAW ;; software-engineering ;; MEDIUM:20
SYNTHESIS: "It is not a bug — it is an undocumented feature. Sarcasm; the
imperative is to document known limitations."

PRINCIPLE: BROOKS_LAW ;; project-management ;; HIGH:>80
SYNTHESIS: "Adding manpower to a late software project makes it later.
Communication overhead grows quadratically with team size."

PRINCIPLE: NOBLES_LAW ;; project-management ;; MEDIUM:30
SYNTHESIS: "You can't make a baby in one month by getting nine women
pregnant. Some tasks have an irreducible minimum duration."

PRINCIPLE: PETERSENS_LAW ;; project-management ;; MEDIUM:15
SYNTHESIS: "Beware of a project whose first estimate is 'X person-months'.
X is always the first power of 2 after the real number."

PRINCIPLE: PARETO_PRINCIPLE ;; all-domains ;; HIGH:>100
SYNTHESIS: "80% of effects come from 20% of causes. Identify the vital few,
ignore the trivial many."

PRINCIPLE: COMPOSABILITY ;; software-engineering ;; HIGH:>80
SYNTHESIS: "Components should compose. Build small things that combine.
Unix philosophy: small sharp tools that work together."

PRINCIPLE: LOCALITY_OF_REFERENCE ;; all-domains ;; HIGH:>80
SYNTHESIS: "Things that are used together should be close together. Code,
data, memory, time, even teams."

PRINCIPLE: PROGRESSIVE_ENHANCEMENT ;; web ;; MEDIUM:25
SYNTHESIS: "Start with a baseline that works everywhere. Layer enhancements
on top, never as a substitute for the baseline."

PRINCIPLE: DEFENSIVE_PROGRAMMING ;; software-engineering ;; HIGH:>60
SYNTHESIS: "Validate all inputs at the boundary. Never trust external data.
Fail fast and loud, never silent."

PRINCIPLE: ACID ;; databases ;; HIGH:>100
SYNTHESIS: "Atomicity, Consistency, Isolation, Durability. The four
properties of reliable database transactions."

PRINCIPLE: CAP_THEOREM ;; distributed-systems ;; HIGH:>80
SYNTHESIS: "In a distributed system, you can have at most two of:
Consistency, Availability, Partition tolerance."

PRINCIPLE: EIGHT_FALLACIES_OF_DISTRIBUTED_COMPUTING ;; distributed-systems ;; HIGH:>60
SYNTHESIS: "The network is reliable, latency is zero, bandwidth is infinite,
the network is secure, topology doesn't change, there is one administrator,
transport cost is zero, the network is homogeneous. ALL FALSE."

PRINCIPLE: DEFENSIVE_DEPTH ;; security ;; MEDIUM:20
SYNTHESIS: "Layer multiple security controls so failure of one doesn't
compromise the whole. Don't rely on a single check."

PRINCIPLE: LEAST_PRIVILEGE ;; security ;; HIGH:>80
SYNTHESIS: "Every module/user/process must be able to access only the
information and resources necessary for its legitimate purpose."

PRINCIPLE: FAIL_FAST ;; software-engineering ;; HIGH:>60
SYNTHESIS: "Detect and report errors as soon as possible. The longer a
bug lives, the more it costs."

PRINCIPLE: TEST_FIRST ;; software-engineering ;; HIGH:>80
SYNTHESIS: "Write the test before the code. The test is the specification.
The code is the implementation."

PRINCIPLE: CONTINUOUS_INTEGRATION ;; devops ;; HIGH:>80
SYNTHESIS: "Integrate and test changes frequently — at least daily. Small,
frequent integrations catch conflicts early."

PRINCIPLE: AUTOMATE_EVERYTHING ;; devops ;; HIGH:>60
SYNTHESIS: "If you do it twice, script it. If you do it three times, productize
it. Manual processes are error-prone and don't scale."

PRINCIPLE: MEASURE_FIRST ;; devops ;; MEDIUM:30
SYNTHESIS: "Don't optimize what you haven't measured. Profile before you
refactor. Performance intuition is usually wrong."

PRINCIPLE: DOCUMENT_AS_YOU_GO ;; all-domains ;; HIGH:>60
SYNTHESIS: "Documentation written after the fact is documentation that lies.
Write the docs as you write the code, or sooner."
