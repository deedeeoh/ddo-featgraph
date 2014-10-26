'''
Test parsing against snippets from Ron's Character Planner data
'''
import unittest
from feat_graph import Feat

class TestParse(unittest.TestCase):


    def test_parse_name(self):
        lines = '''FEATNAME: Abundant Step;
FEATDESCRIPTION: You are able to leap through the air to bring the fight to your enemies or traverse chasms that make normal adventurers balk.;
CLASSLIST: Monk;
LEVEL: 12;
ACQUIRE: Automatic;
ICON: AbundantStepIcon;
'''
        feat = Feat.from_text(lines)
        self.assertEqual("Abundant Step", feat.full_name)
        
    def test_parse_parentheading(self):
        lines = '''PARENTHEADING: Greater Weapon Focus;
FEATNAME: Bludgeoning Weapons;
FEATDESCRIPTION: Provides a +1 bonus to attack rolls when using a bludgeoning weapon, including attacks from a druid in animal form. This bonus stacks with the Weapon Focus feat.;
FEATTAG: Fighter Bonus;
CLASSLIST: Fighter;
LEVEL: 8;
ACQUIRE: Train;
NEEDSALL: Feat Weapon Focus: Bludgeoning Weapons;
ICON: GreaterWeaponFocusIcon;
VERIFIED: 2012-06-26, in-game;
'''
        feat = Feat.from_text(lines)
        self.assertEqual("Greater Weapon Focus: Bludgeoning Weapons", feat.full_name)

    def test_parse_dependencies(self):
        lines = '''FEATNAME: Greater Two Weapon Fighting;
FEATDESCRIPTION: Increases the chance to produce off hand attacks when fighting with two weapons (or as an unarmed monk) by an additional 20% to 80%.;
FEATTAG: Fighter Bonus;
CLASSLIST: Fighter, Paladin, Barbarian, Monk, Rogue, Ranger, Ranger, Cleric, Wizard, Sorcerer, Bard, Favored Soul, Artificer, Druid;
LEVEL: 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1;
ACQUIRE: Train, Train, Train, Train, Train, Train, AutoNoPrereq, Train, Train, Train, Train, Train, Train, Train;
NEEDSALL: Ability Dexterity 17, BAB 11, Feat Improved Two Weapon Fighting;
ICON: GreaterTwoWeaponFightingIcon;
VERIFIED: 2012-06-26, in-game;
'''
        feat = Feat.from_text(lines)
        self.assertEqual(["Improved Two Weapon Fighting"], feat.feat_deps)
        
        lines = '''PARENTHEADING: Greater Weapon Specialization;
FEATNAME: Slashing Weapons;
FEATDESCRIPTION: Provides a +2 bonus to damage rolls when using a slashing weapon. This bonus stacks with the Weapon Specialization feat.;
FEATTAG: Fighter Bonus;
CLASSLIST: Fighter;
LEVEL: 12;
ACQUIRE: Train;
NEEDSALL: Feat Weapon Focus: Slashing Weapons, Feat Weapon Specialization: Slashing Weapons;
ICON: GreaterWeaponSpecializationIcon;
VERIFIED: 2012-06-26, in-game;
'''
        feat = Feat.from_text(lines)
        self.assertEqual(["Weapon Focus: Slashing Weapons", "Weapon Specialization: Slashing Weapons"], feat.feat_deps)
        
        lines = '''FEATNAME: Trapmaking;
FEATDESCRIPTION: You have learned enough about traps to be able to scavenge parts from them, and with the help of the Free Agents, can craft your own.;
CLASSLIST: Rogue, Rogue, Artificer;
LEVEL: 1, 4, 4;
ACQUIRE: Train, AutoNoPrereq, AutoNoPrereq;
NEEDSALL: Feat Trapfinding;
NEEDSONE: Feat Skill Focus: Disable Device, Feat Nimble Fingers, Feat Least Dragonmark of Making;
ICON: TrapFindingIcon;
VERIFIED: 2012-06-26, in-game;
'''
        feat = Feat.from_text(lines)
        self.assertEqual(["Skill Focus: Disable Device", "Nimble Fingers", "Least Dragonmark of Making"], [d.dep for d in feat.or_deps])


if __name__ == "__main__":
    unittest.main()
