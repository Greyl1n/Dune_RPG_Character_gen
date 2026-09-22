"""Drives, Drive Statements, and Ambitions from Dune: Adventures in the Imperium (p. 104-107)."""

from typing import Dict, List
from dune_char_gen.models.enums import DriveName

DRIVE_DESCRIPTIONS: Dict[DriveName, str] = {
    DriveName.DUTY: (
        "Duty reflects your commitment to a person, organization, House, or cause. "
        "It defines obedience, loyalty, obligation, and fulfillment of one's sworn station."
    ),
    DriveName.FAITH: (
        "Faith reflects your belief in something greater than yourself—be it religion, prophecy, "
        "destiny, the philosophy of your school, or trust in personal spiritual convictions."
    ),
    DriveName.JUSTICE: (
        "Justice reflects your belief in fairness, balance, and righting perceived wrongs. "
        "It can represent upholding Imperial law, personal vendetta (kanly), or equity for the downtrodden."
    ),
    DriveName.POWER: (
        "Power reflects your desire to command, control, influence, and dominate your surroundings "
        "and those within them, proving strength, superiority, or securing autonomy."
    ),
    DriveName.TRUTH: (
        "Truth reflects your pursuit of objective reality, knowledge, clarity, and the unmasking of deception. "
        "It values empirical evidence, precision, or philosophical honesty over dogma."
    ),
}

DRIVE_STATEMENTS: Dict[DriveName, List[str]] = {
    DriveName.DUTY: [
        "People are the true strength of a Great House.",
        "I serve at the pleasure of the House.",
        "Humans live best when each has their place.",
        "Acceptance of place is the death of freedom.",
        "Those above offer duty to those below.",
        "I know my responsibilities.",
        "Duty is a sharp blade.",
        "What must be done, must be done.",
        "My House's honor is my honor.",
        "Loyalty is the only currency that never devalues.",
    ],
    DriveName.FAITH: [
        "My faith gives me certainty where others might doubt.",
        "Faith is merely obedience to the myths of the past.",
        "God will deliver me to whatever fate is mine.",
        "Machines are things of corruption.",
        "I trust my heart, not my head.",
        "Our trials are how God tests us.",
        "Those who doubt my faith will be proved wrong.",
        "God has forgotten us for we are not worthy.",
        "The desert cleanses all falsehoods.",
        "Prophecy is written across the stars.",
    ],
    DriveName.JUSTICE: [
        "I must shield those in my care.",
        "I will get revenge on those who have wronged me.",
        "I have no patience for those who complain that life is unfair.",
        "What we do will return to us.",
        "Life isn't fair.",
        "Justice is what you can get away with.",
        "Justice is only for the wealthy.",
        "Everyone should be treated equally.",
        "Kanly must be satisfied in blood and coin.",
        "An eye for an eye restores cosmic balance.",
    ],
    DriveName.POWER: [
        "Power must be used wisely and cleverly.",
        "The power to destroy a thing is the absolute control over it.",
        "All power invites challenge.",
        "Those who have true power need seldom wield it.",
        "Power attracts those who are corruptible.",
        "Power comes at a knife's edge.",
        "I will have what is owed to me.",
        "Strength is nothing without grace.",
        "He who controls the spice controls the universe.",
        "Rule through fear leaves no room for hesitation.",
    ],
    DriveName.TRUTH: [
        "Respect for the truth comes close to being the basis for all morality.",
        "I decide what is true.",
        "I seek to uncover the many secrets of the universe.",
        "If I do not know it, it is irrelevant.",
        "The purpose of argument is to change the nature of truth.",
        "What one wishes were true is seldom so.",
        "You will know me by my deeds.",
        "Truth is the first casualty of war.",
        "The mind unclouded sees the hidden path.",
        "A lie spoken often enough does not become fact.",
    ],
}

AMBITION_EXAMPLES: Dict[DriveName, List[str]] = {
    DriveName.DUTY: [
        "Elevate my House to a seat on the Landsraad High Council.",
        "Safeguard the young Heir from all assassins and political traps.",
        "Restore our House's ancient ancestral homeworld.",
        "Prove myself worthy of succeeding the Warmaster.",
        "Break the bonds of serfdom and forge a new free charter.",
    ],
    DriveName.FAITH: [
        "Fulfill the ancient prophecy of the Mahdi on Arrakis.",
        "Root out Butlerian tech-heresy across three planetary systems.",
        "Attain true spiritual enlightenment through rigorous desert isolation.",
        "Spread the sacred tenets of the Zensunni wanderers.",
        "Expose a false religious movement manipulated by rival Houses.",
    ],
    DriveName.JUSTICE: [
        "Avenge the slaughter of my kin in an honorable kanly feud.",
        "Overturn an unlawful Imperial seizure of our family's mineral fief.",
        "Bring a corrupt CHOAM auditor to trial before the Emperor.",
        "Liberate the enslaved miners of an illicit spice operation.",
        "Establish an inviolable court of arbitration between warring Houses.",
    ],
    DriveName.POWER: [
        "Secure direct control over a profitable spice-harvesting concession.",
        "Become the chief spymaster behind the planetary governor.",
        "Outmaneuver and supplant our bitter rival in the Landsraad.",
        "Master the secrets of the Voice to compel noble peers without question.",
        "Amass enough wealth to purchase a permanent CHOAM directorship.",
    ],
    DriveName.TRUTH: [
        "Expose the treasonous conspiracy linking House rivals to Imperial conspirators.",
        "Decipher an ancient Pre-Guild data crystal lost in the deep sands.",
        "Catalog the exact ecological lifecycle of the great sandworms.",
        "Unmask the undercover Bene Gesserit agent manipulating our court.",
        "Discover the mathematical theorem governing foldspace anomalies.",
    ],
}
