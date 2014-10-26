#!/usr/bin/env python
'''
Create a depencency graph for Dungeons and Dragons Online (DDO)
character feats using FeatsFile.txt from Ron's Character Planner
found at http://www.rjcyberware.com/DDO/

:usage:
python feat_graph.py path/to/DDOCharGenFolder
'''
import sys
import os
import pygraphviz as pgv

class Dependency(object):
    def __init__(self, deptype, dep):
        self.deptype = deptype
        self.dep = dep


class Feat(object):
    FEATS = []
    def __init__(self, name=None, parent_heading=None, deps=None,
                 or_deps=None, automatic=False):
        self.name = name
        self.parent_heading = parent_heading
        if deps is None:
            self.deps = []
        else:
            self.deps = deps
        if or_deps is None:
            self.or_deps = []
        else:
            self.or_deps = or_deps
        self.automatic = automatic
        self.FEATS.append(self)
    
    @property
    def full_name(self):
        if self.parent_heading is None:
            return self.name
        else:
            return "{parent}: {name}".format(parent=self.parent_heading, name=self.name)
        
    @property
    def feat_deps(self):
        return [ dep.dep for dep in self.deps if dep.deptype == "Feat" ]
     
    @classmethod
    def from_text(cls, lines):
        feat = cls()
        for line in lines.splitlines():
            line = line.strip()
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            value = value.strip().rstrip(";")
            if key == "FEATNAME":
                feat.name = value
            elif key == "PARENTHEADING":
                feat.parent_heading = value
            elif key == "NEEDSALL":
                deplist = [ i.strip() for i in value.split(",") ]
                for dep in deplist:
                    dep_type, dep = dep.split(" ", 1)
                    feat.deps.append(Dependency(dep_type, dep))
            elif key == "NEEDSONE":
                deplist = [ i.strip() for i in value.split(",") ]
                for dep in deplist:
                    dep_type, dep = dep.split(" ", 1)
                    feat.or_deps.append(Dependency(dep_type, dep))
            elif key == "ACQUIRE":
                non_auto = [ i.strip() for i in value.split(",") if i.strip() != "Automatic"]
                if non_auto == []:
                    feat.automatic = True
        return feat


def main():
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        filepath = os.path.join(sys.argv[1], "DataFiles", "FeatsFile.txt")
        with open(filepath, "rb") as featfile:
            lines = ""
            for line in featfile:
                if line.isspace():
                    feat = Feat.from_text(lines)
                    #if not feat.automatic:
                        #print feat.full_name, [d.deptype+d.dep for d in feat.deps]
                    lines = ""
                else:
                    lines = lines + line
    else:
        sys.stderr.write("Usage: feat_graph.py path/to/DDOCharGenFolder\n")
        sys.exit(1)
       
    if os.path.basename(sys.argv[1]).startswith("DDOCharGen"):
        planner_version = "version " + os.path.basename(sys.argv[1])[10:]
    else:
        planner_version = ""

    graph = pgv.AGraph(directed=True)
    graph.graph_attr["label"] = ("DDO feat dependency graph by stoerm\n"
                                 "Idea by Peter_Principle and unbongwah\n"
                                 "Data from Ron's Character Planner {0}\n"
                                 "Cool kids don't dupe").format(planner_version)
    graph.graph_attr["rankdir"]  = "LR"
    graph.node_attr["fontsize"]  = 10
    seen = []
    for feat in feat.FEATS:
        if len(feat.deps) > 0 or len(feat.or_deps) > 0:
            graph.add_node(feat.full_name, shape="rectangle")
            seen.append(feat.full_name)
        for dep in feat.deps:
            if dep.deptype in ("Feat", "Epic:"):
                graph.add_node(feat.full_name, shape="rectangle")
                if dep.dep not in seen:
                    graph.add_node(dep.dep, shape="rectangle")
                    seen.append(dep.dep)
            if dep.deptype in ("Feat", "Epic:", "Ability", "Class", "Race"):
                graph.add_edge(dep.dep, feat.full_name)
            else:
                graph.add_edge(dep.deptype+dep.dep, feat.full_name)
        if len(feat.or_deps) > 0:
            deptxt="One of:\n"
            for dep in feat.or_deps:
                if dep.deptype in ("Feat", "Epic:", "Ability", "Class", "Race"):
                    deptxt += dep.dep+"\n"
                else:
                    deptxt += dep.deptype+dep.dep+"\n"
            deptxt = deptxt.rstrip(",")
            graph.add_node(deptxt, shape="rectangle")
            graph.add_edge(deptxt, feat.full_name)

    graph.layout("dot")
    graph.draw('feats_dot.png')
    
                    
if __name__ == '__main__':
    main()
