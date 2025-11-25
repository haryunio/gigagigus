import sys
from PyQt5 import QtWidgets, QtCore
from main_logic import Character, Skill, best_action, judge, apply_damage

class SkillInput(QtWidgets.QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QtWidgets.QLabel(f"{title}:")
        label.setMinimumWidth(50)
        
        self.atk = QtWidgets.QSpinBox(); self.atk.setRange(0, 999); self.atk.setMaximumWidth(60)
        self.def_ = QtWidgets.QSpinBox(); self.def_.setRange(0, 999); self.def_.setMaximumWidth(60)
        
        # Stamina slider (0, 1, 2, 3)
        self.stamina = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.stamina.setRange(0, 3)
        self.stamina.setValue(3)
        self.stamina.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.stamina.setTickInterval(1)
        self.stamina.setMaximumWidth(80)
        
        self.stamina_label = QtWidgets.QLabel("3")
        self.stamina_label.setMaximumWidth(15)
        self.stamina.valueChanged.connect(lambda v: self.stamina_label.setText(str(v)))

        layout.addWidget(label)
        layout.addWidget(QtWidgets.QLabel("ATK"))
        layout.addWidget(self.atk)
        layout.addWidget(QtWidgets.QLabel("DEF"))
        layout.addWidget(self.def_)
        layout.addWidget(QtWidgets.QLabel("Stm"))
        layout.addWidget(self.stamina)
        layout.addWidget(self.stamina_label)
        layout.addStretch()

        self.setLayout(layout)

    def get(self):
        return {"atk": self.atk.value(), "def": self.def_.value(), "stamina": self.stamina.value()}


class CharacterInput(QtWidgets.QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        layout = QtWidgets.QVBoxLayout()

        # HP and Shield section - more compact
        stats_layout = QtWidgets.QGridLayout()
        
        self.hp = QtWidgets.QSpinBox(); self.hp.setRange(1, 999); self.hp.setValue(10); self.hp.setMaximumWidth(70)
        self.max_hp = QtWidgets.QSpinBox(); self.max_hp.setRange(1, 999); self.max_hp.setValue(10); self.max_hp.setMaximumWidth(70)
        self.shield = QtWidgets.QSpinBox(); self.shield.setRange(0, 999); self.shield.setValue(10); self.shield.setMaximumWidth(70)
        self.max_shield = QtWidgets.QSpinBox(); self.max_shield.setRange(0, 999); self.max_shield.setValue(10); self.max_shield.setMaximumWidth(70)
        
        # Enforce max limits
        self.max_hp.valueChanged.connect(lambda v: self.hp.setMaximum(v))
        self.max_shield.valueChanged.connect(lambda v: self.shield.setMaximum(v))
        # Initial constraint
        self.hp.setMaximum(self.max_hp.value())
        self.shield.setMaximum(self.max_shield.value())
        
        stats_layout.addWidget(QtWidgets.QLabel("HP:"), 0, 0)
        stats_layout.addWidget(self.hp, 0, 1)
        stats_layout.addWidget(QtWidgets.QLabel("/ Max:"), 0, 2)
        stats_layout.addWidget(self.max_hp, 0, 3)
        
        stats_layout.addWidget(QtWidgets.QLabel("Shield:"), 1, 0)
        stats_layout.addWidget(self.shield, 1, 1)
        stats_layout.addWidget(QtWidgets.QLabel("/ Max:"), 1, 2)
        stats_layout.addWidget(self.max_shield, 1, 3)
        
        layout.addLayout(stats_layout)
        
        # Skills section - compact horizontal layout
        skills_group = QtWidgets.QGroupBox("Skills")
        skills_layout = QtWidgets.QVBoxLayout()
        skills_layout.setSpacing(5)
        
        self.skill_sword = SkillInput("Sword")
        self.skill_shield = SkillInput("Shield")
        self.skill_spell = SkillInput("Spell")
        
        skills_layout.addWidget(self.skill_sword)
        skills_layout.addWidget(self.skill_shield)
        skills_layout.addWidget(self.skill_spell)
        skills_group.setLayout(skills_layout)
        
        layout.addWidget(skills_group)

        self.setLayout(layout)

    def get_character(self):
        skills = {
            Skill.SWORD: self.skill_sword.get(),
            Skill.SHIELD: self.skill_shield.get(),
            Skill.SPELL: self.skill_spell.get()
        }
        char = Character(self.hp.value(), self.shield.value(), skills, self.max_shield.value())
        # Store max_hp as an attribute for display purposes only
        char.max_hp = self.max_hp.value()
        return char


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GigaGigus - Combat Calculator")

        main_layout = QtWidgets.QVBoxLayout()
        
        # Character inputs side by side
        chars_layout = QtWidgets.QHBoxLayout()
        self.my_input = CharacterInput("My Stats")
        self.enemy_input = CharacterInput("Enemy Stats")
        chars_layout.addWidget(self.my_input)
        chars_layout.addWidget(self.enemy_input)
        
        main_layout.addLayout(chars_layout)

        # Button and result
        self.button = QtWidgets.QPushButton("Calculate Best Move")
        self.button.clicked.connect(self.calculate)
        
        self.result_label = QtWidgets.QLabel("Result")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        font = self.result_label.font()
        font.setPointSize(12)
        font.setBold(True)
        self.result_label.setFont(font)
        
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.result_label)
        
        # Collapsible details section
        self.details_group = QtWidgets.QGroupBox("Detailed Breakdown")
        self.details_group.setCheckable(True)
        self.details_group.setChecked(False)  # Initially collapsed
        self.details_group.toggled.connect(self.on_details_toggled)
        
        details_layout = QtWidgets.QVBoxLayout()
        self.detail_text = QtWidgets.QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setPlaceholderText("Detailed breakdown will appear here...")
        self.detail_text.setMinimumHeight(250)
        details_layout.addWidget(self.detail_text)
        
        self.details_group.setLayout(details_layout)
        self.details_group.setVisible(False)  # Hidden initially
        
        main_layout.addWidget(self.details_group)

        self.setLayout(main_layout)
    
    def on_details_toggled(self, checked):
        """Handle the details section toggle"""
        if checked:
            self.details_group.setVisible(True)
            self.adjustSize()
        else:
            self.details_group.setVisible(False)
            self.adjustSize()

    def calculate(self):
        me = self.my_input.get_character()
        enemy = self.enemy_input.get_character()

        best, ev = best_action(me, enemy)
        self.result_label.setText(f"Best Skill: {best.name}  |  Expected Value (EV): {ev:.2f}")
        
        # Generate detailed breakdown
        self.show_detailed_breakdown(me, enemy, best)
        
        # Auto-expand details section after calculation
        if not self.details_group.isChecked():
            self.details_group.setChecked(True)
    
    def show_detailed_breakdown(self, my_char: Character, enemy_char: Character, my_skill: Skill):
        """Show detailed breakdown of all possible outcomes for the best skill"""
        
        # Check if skill is available
        if my_char.skills[my_skill]["stamina"] <= 0:
            self.detail_text.setText(f"⚠️ {my_skill.name} is not available (stamina = 0)")
            return
        
        # Get available enemy skills
        enemy_available = [s for s in Skill if enemy_char.skills[s]["stamina"] > 0]
        if not enemy_available:
            self.detail_text.setText("No enemy skills available.")
            return
        
        probability = 1.0 / len(enemy_available)
        
        details = []
        details.append(f"=== EV Calculation Breakdown for {my_skill.name} ===\n")
        details.append(f"My Stats: HP={my_char.hp}/{my_char.max_hp}, Shield={my_char.shield}/{my_char.max_shield}")
        details.append(f"Enemy Stats: HP={enemy_char.hp}/{enemy_char.max_hp}, Shield={enemy_char.shield}/{enemy_char.max_shield}\n")
        details.append(f"Enemy has {len(enemy_available)} available skill(s): {', '.join(s.name for s in enemy_available)}")
        details.append(f"Each outcome has probability: {probability:.2%}\n")
        details.append("=" * 60 + "\n")
        
        total_ev = 0
        
        for i, es in enumerate(enemy_available, 1):
            # Simulate this outcome
            me_sim = Character(my_char.hp, my_char.shield, my_char.skills, my_char.max_shield)
            enemy_sim = Character(enemy_char.hp, enemy_char.shield, enemy_char.skills, enemy_char.max_shield)
            
            my_atk = me_sim.skills[my_skill]["atk"]
            my_def = me_sim.skills[my_skill]["def"]
            enemy_atk = enemy_sim.skills[es]["atk"]
            enemy_def = enemy_sim.skills[es]["def"]
            
            # Record initial state
            my_hp_before = me_sim.hp
            my_shield_before = me_sim.shield
            enemy_hp_before = enemy_sim.hp
            enemy_shield_before = enemy_sim.shield
            
            # Determine matchup result
            win_result = judge(my_skill, es)
            
            # Apply matchup-based rules
            if win_result == 1:
                # I win: Only my attack and shield apply
                apply_damage(enemy_sim, my_atk)
                me_sim.shield = min(me_sim.shield + my_def, me_sim.max_shield)
                matchup = "✓ WIN"
            elif win_result == -1:
                # I lose: Only enemy attack and shield apply
                apply_damage(me_sim, enemy_atk)
                enemy_sim.shield = min(enemy_sim.shield + enemy_def, enemy_sim.max_shield)
                matchup = "✗ LOSE"
            else:
                # Draw: Both attacks and shields apply
                apply_damage(enemy_sim, my_atk)
                apply_damage(me_sim, enemy_atk)
                me_sim.shield = min(me_sim.shield + my_def, me_sim.max_shield)
                enemy_sim.shield = min(enemy_sim.shield + enemy_def, enemy_sim.max_shield)
                matchup = "= DRAW"
            
            # Calculate damage and net value (including shield)
            enemy_hp_lost = enemy_hp_before - enemy_sim.hp
            enemy_shield_lost = enemy_shield_before - enemy_sim.shield
            my_hp_lost = my_hp_before - me_sim.hp
            my_shield_lost = my_shield_before - me_sim.shield
            
            net_value = (enemy_hp_lost + enemy_shield_lost) - (my_hp_lost + my_shield_lost)
            total_ev += net_value * probability
            
            details.append(f"Case {i}: Enemy uses {es.name} {matchup}")
            details.append(f"  Probability: {probability:.2%}")
            details.append(f"  My Action: ATK={my_atk}, DEF={my_def}")
            details.append(f"  Enemy Action: ATK={enemy_atk}, DEF={enemy_def}")
            details.append(f"  ")
            details.append(f"  My State Change:")
            details.append(f"    HP: {my_hp_before}/{my_char.max_hp} → {me_sim.hp}/{my_char.max_hp} (Δ{me_sim.hp - my_hp_before:+d})")
            details.append(f"    Shield: {my_shield_before}/{my_char.max_shield} → {me_sim.shield}/{my_char.max_shield} (Δ{me_sim.shield - my_shield_before:+d})")
            details.append(f"  ")
            details.append(f"  Enemy State Change:")
            details.append(f"    HP: {enemy_hp_before}/{enemy_char.max_hp} → {enemy_sim.hp}/{enemy_char.max_hp} (Δ{enemy_sim.hp - enemy_hp_before:+d})")
            details.append(f"    Shield: {enemy_shield_before}/{enemy_char.max_shield} → {enemy_sim.shield}/{enemy_char.max_shield} (Δ{enemy_sim.shield - enemy_shield_before:+d})")
            details.append(f"  ")
            details.append(f"  📊 Enemy Lost: HP={enemy_hp_lost}, Shield={enemy_shield_lost} (Total: {enemy_hp_lost + enemy_shield_lost})")
            details.append(f"  📊 My Lost: HP={my_hp_lost}, Shield={my_shield_lost} (Total: {my_hp_lost + my_shield_lost})")
            details.append(f"  💰 Net Value: {enemy_hp_lost + enemy_shield_lost} - {my_hp_lost + my_shield_lost} = {net_value:+.0f}")
            details.append(f"  📈 Contribution to EV: {net_value:+.0f} × {probability:.2%} = {net_value * probability:+.2f}")
            details.append("")
        
        details.append("=" * 60)
        details.append(f"💯 Total Expected Value (EV): {total_ev:.2f}")
        details.append(f"   (Sum of all contributions from {len(enemy_available)} cases)")
        
        self.detail_text.setText("\n".join(details))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(800, 450)  # Smaller initial size
    w.show()
    sys.exit(app.exec_())