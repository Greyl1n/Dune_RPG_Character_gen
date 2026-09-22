"""Canonical Talents catalog from Dune: Adventures in the Imperium (p. 126-133)."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from dune_char_gen.models.enums import FactionType, SkillName, DriveName


@dataclass(frozen=True)
class TalentDefinition:
    name: str
    faction_requirement: Optional[str]
    skill_param: bool
    drive_param: bool
    flavor: str
    rules: str


TALENTS: Dict[str, TalentDefinition] = {
    'Adrenaline Shot': TalentDefinition(
        name='Adrenaline Shot',
        faction_requirement='Suk Doctor',
        skill_param=False,
        drive_param=False,
        flavor='You are adept at getting people back on their feet, even',
        rules='if you only make them forget their pain for a moment. By using an action, the character can remove the effects of any physical complication from a character who is in the same zone. This complication is not removed and returns at the end of the scene unless otherwise removed. This talent can only be used once on a given character during each scene, but can be used on each character.',
    ),
    'Advisor': TalentDefinition(
        name='Advisor',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor="You've got a knack for guiding others through problems.",
        rules='When you choose this talent, select a single skill. When ever you assist an ally and you use that skill, the ally you assist may re-roll a single d20 in their dice pool.',
    ),
    'Binding Promise': TalentDefinition(
        name='Binding Promise',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Whether through your demeanor, your reputation,',
        rules='or the method of your persuasion, you have a way of making people reluctant to break faith with you. When you succeed at a Communicate test to persuade someone to agree to a promise or agreement, you may spend one, two, or three points of Momentum to make that agreement binding. If that person wishes to break the promise, they must spend Threat equal to twice the Momentum you spent.',
    ),
    'Bold': TalentDefinition(
        name='Bold',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor='When you take calculated risks, you tend to succeed',
        rules='more often than seems reasonable. When you select this talent, choose a single skill. When you attempt a test using the chosen skill, and you buy additional d20s by generating Threat for the gamemaster, you may re-roll a single d20 in that dice pool.',
    ),
    'Bolster': TalentDefinition(
        name='Bolster',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your certainty and resolve are a beacon to others, who',
        rules='might waver without your example. Once per scene, when an ally fails a skill test, you may immediately spend 2 points of Momentum or add 2 to Threat to allow that ally to re-roll their dice pool. When they re-roll, they may use your Discipline score instead of the skill they were using.',
    ),
    'Calculated Prediction': TalentDefinition(
        name='Calculated Prediction',
        faction_requirement='Mentat',
        skill_param=False,
        drive_param=False,
        flavor='Using the facts and figures you have memorized and',
        rules='your ability to process information, you can attempt to predict the future. No such predictions are 100% per fect, as there may be variables you are unaware of that affect the future. You may spend a few minutes to meditate upon predict ing the future. This requires an Understand test with a Difficulty of 4; if successful, you may ask the Gamemas ter to state something that is likely to occur in the future. You may ask for one additional prediction for every two points of Momentum you spend. The Gamemaster can make these predictions vague and they do not have to explain any context for the prediction or why that thing is likely to occur.',
    ),
    'Cautious': TalentDefinition(
        name='Cautious',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor='You are patient and circumspect, acting only when the',
        rules='odds are in your favor. When you select this talent, choose a single skill. When you attempt a test using that skill, and you buy addi tional d20s by spending Momentum, you may re-roll a single d20 in that dice pool.',
    ),
    'Collaboration': TalentDefinition(
        name='Collaboration',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor="You've coached your allies to capitalize on your exper",
        rules='tise, and that effort has paid off. When you select this talent, choose a single skill with a rating of 6 or more. Whenever an ally attempts a test using that skill, and you can communicate with them, you may spend 2 points of Momentum to allow them to use your score for that skill, and one of your focuses (if applicable).',
    ),
    'Combat Medic': TalentDefinition(
        name='Combat Medic',
        faction_requirement='Suk Doctor',
        skill_param=False,
        drive_param=False,
        flavor='You are skilled at offering rapid medical attention, even',
        rules='during a battle. When an ally in combat has suffered points towards the requirement to defeat them, you may spend 1 point of Momentum to reduce that point total by 2 as an action.',
    ),
    'Constantly Watching': TalentDefinition(
        name='Constantly Watching',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="You're vigilant, bordering on paranoid… and little",
        rules='catches you off-guard. Whenever you attempt a skill test to detect danger or hidden enemies, you reduce the Difficulty by 2, to a minimum of 0. In addition, once per scene, when an enemy chooses to Keep the Initiative, you can increase the cost to do so by +2.',
    ),
    'Cool Under Pressure': TalentDefinition(
        name='Cool Under Pressure',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor='When the situation gets tough, you take a deep breath',
        rules='and get the job done. When you select this talent, choose a single skill. When you attempt a test using that skill, before rolling you may spend a Determination point to automatically succeed at that test, but you generate no Momentum. The normal conditions for spending Determination still apply.',
    ),
    'Decisive Action': TalentDefinition(
        name='Decisive Action',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You take risks in combat, often ones that seem fool',
        rules="hardy or needless. You have a knack for making those gambles pay off. In a conflict, when you succeed at a Battle test to remove an opponent's assets, and you bought one or more dice by generating Threat, you may spend 2 points of Momentum to remove a second enemy asset.",
    ),
    'Dedication': TalentDefinition(
        name='Dedication',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your commitment to a cause is unwavering, and this has',
        rules='carried you through many a tough situation. At the start of a scene, if there is no Momentum in the group pool, roll 1d20. If you roll equal to or less than your Discipline score, add 1 to the group Momentum pool.',
    ),
    'Deliberate Motion': TalentDefinition(
        name='Deliberate Motion',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Every step you take is considered, and you are excep',
        rules='tionally sure-footed. When you attempt a Move test and suffer one or more complications, you may spend Momentum to ignore some or all of those complications; this costs 1 point of Momentum per complication ignored.',
    ),
    'Direct': TalentDefinition(
        name='Direct',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your will and presence can drive others to act swiftly',
        rules='and efficiently. Once per scene, you may command an ally or subordi nate to act. This requires no test from you, but the com manded ally may immediately attempt an action of their own, and you may assist any test they attempt. If done during a conflict, the ally acts on your turn regardless of if they have already acted, and this does not prevent them acting later during the round.',
    ),
    'Driven': TalentDefinition(
        name='Driven',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your determination does not waver.',
        rules='After you spend a point of Determination, roll 1d20. If you roll equal to or under your Discipline rating (by itself), you immediately regain that point of Determination.',
    ),
    'Dual Fealty': TalentDefinition(
        name='Dual Fealty',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You owe your service and your life to two different fac',
        rules='tions equally, and you have the trust of both. Choose two factions to be loyal to. This will normally be your House and another group such as the Bene Gesserit, but it can be to any two factions you would reasonably have contact with. Both factions are aware of your loyalties to both and expect that you will not betray one to the other. You may interact on friendly terms with members of both factions, without any expectations of betrayal or other peril.',
    ),
    'Failed Navigator': TalentDefinition(
        name='Failed Navigator',
        faction_requirement='Spacing Guild Agent',
        skill_param=False,
        drive_param=False,
        flavor='You underwent trials to become a Guild Navigator, but you',
        rules='failed to meet the standards required… yet, for one brief moment, your consciousness became one with the uni verse. In times of stress, your mind sometimes repeats this, granting you a momentary insight of some kind. Whenever you spend a point of Determination, the gamemaster will grant you an additional insight. This may relate to your current activities, or it may be com pletely unrelated.',
    ),
    'Find Trouble': TalentDefinition(
        name='Find Trouble',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You know where to find the criminal element wherever',
        rules="you go. Wherever you are, once per adventure, you can always contact the criminal underworld or black market (as long as there is one in that area). This doesn't mean they will be well disposed toward you, just that you can find a contact.",
    ),
    'Guildsman': TalentDefinition(
        name='Guildsman',
        faction_requirement='Spacing Guild Agent',
        skill_param=False,
        drive_param=False,
        flavor='You have connections to the Spacing Guild, granting',
        rules='you more access to their resources than most. You are not a Navigator, but you may be an agent, representa tive, banker, diplomat, or similar associate of the Guild. Once per adventure, you may call upon your Spacing Guild connection to use Guild facilities or resources, or to organize a meeting with important persons within the Guild. You do not have the authority to make demands of the Guild itself. If you need to use Guild resources more than once during the course of an adventure, the second time adds 2 to Threat, the third time adds 4, and so forth, adding +2 to the cost each time, as your increased use risks drawing undue attention to you.',
    ),
    'Hidden Motives': TalentDefinition(
        name='Hidden Motives',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are a master at concealing your intentions and',
        rules='motivations. Few truly know what drives you, even if they think they understand you. When an opponent fails an Understand or Communicate test against you, you may immediately create a trait which reflects a mistaken belief they have about you.',
    ),
    'Hyperawareness': TalentDefinition(
        name='Hyperawareness',
        faction_requirement='Bene Gesserit Sister',
        skill_param=False,
        drive_param=False,
        flavor='Your training has honed your awareness to an incredible',
        rules='degree, allowing you to notice details too small for others to perceive. Armed with these insights, you can uncover secrets and truths that others may be oblivious to. Whenever you spend Momentum to Obtain Informa tion about the current situation, your current location, or a person you can currently observe, you may ask two questions for the first point of Momentum spent. Fur ther, the limits of what others would be able to notice do not apply to you for any questions.',
    ),
    'Imperial Conditioning': TalentDefinition(
        name='Imperial Conditioning',
        faction_requirement='Suk Doctor',
        skill_param=False,
        drive_param=False,
        flavor='Through intense psychological conditioning, you cannot',
        rules='take a human life, or cause a human to come to harm. This is a necessary step, for those with power and status must be free of the fear that their physicians might be assassins. 128 You cannot willingly inflict harm upon or kill a human being. Any attempt to coerce you into such an action auto matically fails, and you automatically succeed on any skill test to persuade another that you intend them no harm.',
    ),
    'Improved Resources': TalentDefinition(
        name='Improved Resources',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are entrusted with greater access to the tools and',
        rules='resources you need to achieve your goals. You may increase the number of assets you possess by +1. This talent may be purchased multiple times.',
    ),
    'Improvised Weapon': TalentDefinition(
        name='Improvised Weapon',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are able to turn the most innocuous items into',
        rules="deadly weapons at a moment's notice. Once per scene you may create a Quality 0 asset (at no cost) that you can use in a personal or skirmish conflict. It might be a rock, broken bottle, or shard of glass, but it is enough to function as a weapon. The asset is removed at the end of any conflict it is used for, as it will be too badly damaged to use again.",
    ),
    'Intense Study': TalentDefinition(
        name='Intense Study',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are extremely well-read, with vast amounts of',
        rules='knowledge about a wide range of subjects. Once per scene, you may use your Understand skill on a single skill test instead of any other skill, and you are counted as having a focus for that test.',
    ),
    'Make Haste': TalentDefinition(
        name='Make Haste',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='There is value in speed, even if there are consequences.',
        rules='When you attempt a Move test, you may choose to suffer one additional complication in exchange for scoring one automatic success on the test. During any conflict, you may add 1 to Threat to take the first action, regardless of who would otherwise act first.',
    ),
    'Mask of Power': TalentDefinition(
        name='Mask of Power',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You can intimate that you know more than you do about',
        rules="an enemy's secrets. Once per scene you may create an asset (at no cost) such as blackmail evidence or an owed favor that will allow you to initiate an intrigue or espionage conflict with a person of your choosing. The asset is a lie, of course; you don't have anything, but your target doesn't know that. The asset is removed once the conflict is over, and if you are defeated the fact you were bluffing is exposed and you suffer an additional complication.",
    ),
    'Master-at-Arms': TalentDefinition(
        name='Master-at-Arms',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your expertise in battle is considerable, and few can',
        rules="match your effectiveness in combat. At the start of a duel, skirmish, or battle scene, select a single asset that represents a melee weapon or a unit of troops. Due to your prowess, you may spend 1 Momen tum to improve that asset's Quality by 1 for the next conflict in this scene.",
    ),
    'Masterful Innuendo': TalentDefinition(
        name='Masterful Innuendo',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You have a special knack for saying more than one thing',
        rules='at once, conveying one message with the literal meaning of your words and another with innuendo, allusions, and signals that only the intended recipients will understand. When you attempt a Communicate test, you may choose to increase the Difficulty of the test by +1 to conceal a hidden message within your words. You must state who is the intended recipient of this hidden mes sage. People other than the intended recipient cannot discern that you have concealed another message, unless they have this talent, or some other ability to detect things which people cannot normally detect (such as the Hyperawareness talent).',
    ),
    'Mentat Discipline': TalentDefinition(
        name='Mentat Discipline',
        faction_requirement='Mentat',
        skill_param=False,
        drive_param=False,
        flavor='Intense mental conditioning and extensive training have',
        rules='developed your intellect into a potent and valuable thing. You can retain and process vast amounts of infor mation at extraordinary speeds. You have almost perfect recall, for even the most com plex data. When making an Understand test that applies to recalling data, one of the D20s in your pool may be considered to have rolled a 1 instead of rolling it.',
    ),
    'Mind Palace': TalentDefinition(
        name='Mind Palace',
        faction_requirement='Mentat',
        skill_param=False,
        drive_param=False,
        flavor='You have exceptional recall and can reconstruct events',
        rules='and places you have experienced with perfect accuracy, allowing you to revisit them later. You may attempt a Difficulty 0 Understand test to recall a past event or a place you have previously been to. Momentum you generate on this test may be spent to recall facts and details about that event or location; this is treated like Obtain Information, but you may ask ques tions about things you have previously encountered, rather than merely those which are currently present in the scene.',
    ),
    'Nimble': TalentDefinition(
        name='Nimble',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="You're quick on your feet, and few obstacles can",
        rules="impede you. When attempting a Move test to move over, around, or through difficult terrain or similar physical obstacles (such as during a duel or skirmish), you may reduce the Difficulty of the test by 2. If this reduces the Difficulty to 0, you may move over or around that obstacle freely as if it wasn't there.",
    ),
    'Other Memory': TalentDefinition(
        name='Other Memory',
        faction_requirement='Bene Gesserit Sister',
        skill_param=False,
        drive_param=False,
        flavor='You have undergone the Agony attended by another',
        rules='Reverent Mother, and now you can draw upon the mem ories and wisdom of all your ancestors. In doing so, you have become a Reverend Mother of the Bene Gesserit. You must be a Reverend Mother of the Bene Gesserit (and have an appropriate trait reflecting this) to select this talent. If this talent is selected in play, another Rev erend Mother must be on hand and in physical contact to pass this genetic memory on to you. Whenever you attempt a test where knowledge of past events—even those which may have occurred many generations ago—would be beneficial, you score three automatic successes. You may also share your genetic memory with other Reverend Mothers at will.',
    ),
    'Passive Scrutiny': TalentDefinition(
        name='Passive Scrutiny',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are quick to notice details which may be of impor',
        rules="tance later. When you enter a scene, you may ask one question of the gamemaster as if you'd spent Momentum to Obtain Information.",
    ),
    'Performer': TalentDefinition(
        name='Performer',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your skill with music or poetry helps to soothe and',
        rules="inspire your comrades. Once per scene you may entertain the group with a short performance. This might be playing the balliset, singing, reciting a poem, dancing, or even juggling. Once the performance is over you may add 1 to the group's Momentum pool.",
    ),
    'Prana-bindu Conditioning': TalentDefinition(
        name='Prana-bindu Conditioning',
        faction_requirement='Bene Gesserit Sister',
        skill_param=False,
        drive_param=False,
        flavor='You have absolute control over your body. Every muscle',
        rules="and every nerve is under your control, and you have even mastered your own body chemistry and metabolism. Whenever you attempt a Move or Discipline test which relies on your control of your body, you may re-roll a single d20. You can perfectly control your breathing, heart rate, and your internal organs (including the ability to choose whether to conceive a child, and to deter mine the child's physical and genetic traits).",
    ),
    'Priority Boarding': TalentDefinition(
        name='Priority Boarding',
        faction_requirement='Spacing Guild Agent',
        skill_param=False,
        drive_param=False,
        flavor='You can call in a few favors to ensure the Guild inspec',
        rules="tors don't take too long looking at your luggage. You don't need to offer bribes to ensure Guild inspec tors simply take your word for it that all your cargo and possessions are as they should be. This allows you to smuggle anything aboard a Guild ship. However, if something you have brought aboard creates problems for the Guild, you will lose this talent.",
    ),
    'Putting Theory into Practice': TalentDefinition(
        name='Putting Theory into Practice',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="You've learned how to quickly turn newfound knowl",
        rules="edge into a practical advantage. Once per scene, when you Obtain Information, you may create a trait for free, which must represent an advantage, opportunity, or weakness you've identified with the information you received.",
    ),
    'Ransack': TalentDefinition(
        name='Ransack',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='When time is of the essence, you prioritize getting the',
        rules='work done over covering your tracks. When you attempt an Understand test to search an area, you may add 2 to Threat to reduce the difficulty of the test by 1, and to halve the amount of time the test takes to attempt.',
    ),
    'Rapid Maneuver': TalentDefinition(
        name='Rapid Maneuver',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="You're fast, able to cross ground, find the shortest",
        rules='route, and bring your tools to bear quicker than most. When attempting a skill test to reach a destination quickly when moving on foot or in a vehicle, reduce the Difficulty by 1. In a conflict, when moving an asset, you may move the asset an additional zone for 1 point of Momentum, rather than 2.',
    ),
    'Rapid Recovery': TalentDefinition(
        name='Rapid Recovery',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You return to fighting form quickly after being injured,',
        rules='even when it may be risky to return to the fray. Once per scene, at the start of your turn, you may add +2 to Threat to remove a complication which represents an injury. In addition, you may pay to Resist Defeat one additional time during a conflict.',
    ),
    'Resilience': TalentDefinition(
        name='Resilience',
        faction_requirement='Fremen',
        skill_param=True,
        drive_param=False,
        flavor='It takes a lot to put you down in a conflict. You get back',
        rules="up more often than most. Usually you may only ‘Resist Defeat' once per scene. You can do so twice per scene, but only when in a conflict using the listed skill.",
    ),
    'Rigorous Control': TalentDefinition(
        name='Rigorous Control',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are an island of calm amidst the chaos of the',
        rules='universe, maintaining control over yourself when you cannot control anything else. Whenever you are attempting an extended task where the requirement is based on one of your skills, at the cost of 1 Momentum you may use your Discipline for that requirement instead of the skill normally used. If the requirement would normally be based on your Discipline, reduce the requirement by 1 for that extended task.',
    ),
    'Specialist': TalentDefinition(
        name='Specialist',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your duties require you to manage a greater type of a',
        rules='specific kind of asset. You may purchase this talent multiple times. Each time you select this talent, choose a single category of asset from the following list: dueling, warfare, espionage, or intrigue. You increase the number of assets you possess by +2, but those two additional assets must be from the chosen category. 130',
    ),
    'Stirring Rhetoric': TalentDefinition(
        name='Stirring Rhetoric',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are an able public speaker, and your words carry',
        rules='weight and purpose. When you succeed at a Communicate test to address a group of people, you may select a number of those people equal to your Communicate skill. Those char acters may re-roll a single d20 on the next test they attempt which uses the same drive that you used on your Communicate test.',
    ),
    'Subtle Step': TalentDefinition(
        name='Subtle Step',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="You're well-versed in methods of avoiding notice, and",
        rules='you reveal little that you do not intend to. When you attempt a Move test to sneak or otherwise pass unseen through an area, or when you attempt to move an asset subtly during a conflict, the first extra d20 you purchase for the test is free.',
    ),
    'Subtle Words': TalentDefinition(
        name='Subtle Words',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='You are skilled at swaying others with a few quiet words',
        rules='spoken in the right place at the right time. Even they may not realize what influence your words have had. When you attempt a Communicate test, and you buy one or more dice by spending Momentum, you may create a new trait for free upon the character you have spoken to, which reflects your influence upon their thoughts or mood.',
    ),
    'The Reason I Fight': TalentDefinition(
        name='The Reason I Fight',
        faction_requirement=None,
        skill_param=False,
        drive_param=True,
        flavor='Skill is not the only factor in determining victory;',
        rules="those who want it more, and those who are driven by a greater sense of purpose, may triumph when they should have failed. When you select this talent, choose a single drive rated 6 or higher. When you attempt a Battle test using the chosen drive, and the drive's statement aligns with the action being attempted, you may re-roll 1d20.",
    ),
    'The Slow Blade': TalentDefinition(
        name='The Slow Blade',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor="The slow blade pierces the shield. You're well-versed in",
        rules="the subtle ways of avoiding an opponent's defenses. When you make an attack during a duel or a skirmish using a melee weapon, and you buy one or more dice by spending Momentum, you may choose one of the enemy's assets in the same zone as your attack; you can ignore that asset during your attack.",
    ),
    'To Fight Someone is to Know Them': TalentDefinition(
        name='To Fight Someone is to Know Them',
        faction_requirement=None,
        skill_param=True,
        drive_param=False,
        flavor='You are an expert in studying your foes in conflict,',
        rules="learning how they think and gleaning secrets from them based on how they move, attack, and defend. When you select this talent, choose a skill. When you win a conflict using the chosen skill, you gain two bonus Momentum points, which you may use to Obtain Infor mation or to create a trait that represents some knowl edge or insight you've gained about your opponent.",
    ),
    'Twisted Mentat': TalentDefinition(
        name='Twisted Mentat',
        faction_requirement='Mentat',
        skill_param=False,
        drive_param=False,
        flavor='Your Mentat abilities were shaped and engineered by',
        rules='the Bene Tleilax to leave you unencumbered by such petty things as morality, taboo, or decency. Whenever you attempt an Understand test, you gen erate one bonus Momentum point for each die you bought by adding to Threat. This bonus Momentum may only be used to Obtain Information about the most effective ways to harm or inflict pain upon a person within the scene, or to create a trait which represents a weakness you have discovered which you can exploit. This Talent may only be chosen in character creation.',
    ),
    'Unquestionable Loyalty': TalentDefinition(
        name='Unquestionable Loyalty',
        faction_requirement=None,
        skill_param=False,
        drive_param=False,
        flavor='Your loyalty to your House is such that it can drive you',
        rules='to action even in the direst of circumstances. At the start of each adventure, you begin with one additional point of Determination. This extra point can only be used on an action which is in direct service to your House.',
    ),
    'Verify': TalentDefinition(
        name='Verify',
        faction_requirement='Mentat',
        skill_param=False,
        drive_param=False,
        flavor='You have so much data at your fingertips you can see',
        rules='where it contradicts and determine where falsehoods lie. You may spend a point of Momentum to ask the gam emaster if a piece of information you have is true or false. You need not be making a skill test as with Obtain Information, and the data can be your supposition as much as a specific document or rumor.',
    ),
    'Voice': TalentDefinition(
        name='Voice',
        faction_requirement='Bene Gesserit Sister',
        skill_param=False,
        drive_param=False,
        flavor='You have been trained to modulate your voice to influ',
        rules='ence the subconscious minds of others. With this skill you can subtly manipulate others, alter motivations and moods, or even compel action from the unwilling. You may use Voice whenever you speak to someone else, though you must be able to observe them for a short while beforehand, and they must be able to hear you speak. When you use Voice, you may add one, two, or three points to Threat to score the same number of automatic successes on any Communicate test made to influence your chosen target. The greater the number of automatic successes, the more overt your use of Voice, which others may notice. Your training also allows you to buy those automatic successes on any test made to resist the effects of Voice.',
    ),
}


def get_talent(name: str) -> Optional[TalentDefinition]:
    """Retrieve talent by name (handles parametrized names like 'Advisor (Battle)')."""
    if name in TALENTS:
        return TALENTS[name]
    base_name = name.split("(")[0].strip()
    return TALENTS.get(base_name)


def get_all_talent_names() -> List[str]:
    return sorted(list(TALENTS.keys()))


def get_talents_for_faction(faction_name: Optional[str]) -> List[TalentDefinition]:
    """Return talents available to the given faction (universal talents + faction-specific)."""
    available = []
    for t in TALENTS.values():
        if t.faction_requirement is None:
            available.append(t)
        elif faction_name and t.faction_requirement.lower() in faction_name.lower():
            available.append(t)
    return sorted(available, key=lambda x: x.name)
