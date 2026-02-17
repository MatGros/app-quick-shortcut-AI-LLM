#!/usr/bin/env python3
"""
Documentation Verification Script - Pre-Release Checklist

Run before each release to ensure documentation is complete and coherent.

Usage:
    python docs/verify_docs.py
    or
    bash docs/verify_documentation.sh
"""

import os
import sys
from pathlib import Path

class DocVerifier:
    def __init__(self):
        self.passed = 0
        self.warnings = 0
        self.errors = 0
        self.repo_root = Path(__file__).parent.parent
        os.chdir(self.repo_root)

    def pass_check(self, msg):
        print(f"✓ {msg}")
        self.passed += 1

    def warn_check(self, msg):
        print(f"⚠ {msg}")
        self.warnings += 1

    def fail_check(self, msg):
        print(f"✗ {msg}")
        self.errors += 1

    def section(self, title):
        print(f"\n{title}")
        print("=" * 60)

    # ========================================================================
    # SECTION 1: STRUCTURE VERIFICATION
    # ========================================================================
    def verify_structure(self):
        self.section("1. STRUCTURE VERIFICATION")

        required_folders = [
            "docs/01_input",
            "docs/02_planning",
            "docs/03_implementation",
            "docs/04_testing",
            "docs/05_review",
            "docs/06_release",
            "docs/07_archive",
        ]

        # Check all 7 folders exist
        for folder in required_folders:
            if Path(folder).is_dir():
                self.pass_check(f"{folder}/ exists")
            else:
                self.fail_check(f"Missing: {folder}/")

        # Check no illegal folders
        illegal_patterns = ["logs", "technical", "archive/", "planning/", "testing/"]
        illegal_found = []
        for item in Path("docs").iterdir():
            if item.is_dir() and not item.name.startswith("."):
                for pattern in illegal_patterns:
                    if pattern in item.name and not item.name.startswith("0"):
                        illegal_found.append(item.name)

        if illegal_found:
            self.fail_check(f"Illegal folders found: {', '.join(illegal_found)}")
        else:
            self.pass_check("No illegal folders (no docs/logs/, docs/technical/, etc.)")

        # Check each folder has README.md
        for folder in required_folders:
            readme = Path(folder) / "README.md"
            if readme.exists():
                self.pass_check(f"{folder}/README.md exists")
            else:
                self.fail_check(f"Missing: {folder}/README.md")

    # ========================================================================
    # SECTION 2: FILE PLACEMENT VALIDATION
    # ========================================================================
    def verify_file_placement(self):
        self.section("2. FILE PLACEMENT VALIDATION")

        # 01_input required files
        input_files = [
            "docs/01_input/CAHIER_DES_CHARGES.md",
            "docs/01_input/SPEC.md",
            "docs/01_input/PROJECT_DEFINITION.md",
        ]
        for f in input_files:
            if Path(f).exists():
                self.pass_check(f"{Path(f).name} in 01_input/")
            else:
                self.fail_check(f"Missing: {f}")

        # 02_planning required files
        planning_files = [
            "docs/02_planning/TODO.md",
            "docs/02_planning/IMPLEMENTATION_PLAN.md",
        ]
        for f in planning_files:
            if Path(f).exists():
                self.pass_check(f"{Path(f).name} in 02_planning/")
            else:
                self.fail_check(f"Missing: {f}")

        # 03_implementation
        if Path("docs/03_implementation/TECHNICAL_DECISIONS.md").exists():
            self.pass_check("TECHNICAL_DECISIONS.md in 03_implementation/")
        else:
            self.fail_check("Missing: docs/03_implementation/TECHNICAL_DECISIONS.md")

        # 04_testing required files
        testing_files = [
            "docs/04_testing/QUICK_START_TESTS.md",
            "docs/04_testing/VSCODE_TESTING_GUIDE.md",
            "docs/04_testing/UAT_DETAILED_GUIDE.md",
        ]
        for f in testing_files:
            if Path(f).exists():
                self.pass_check(f"{Path(f).name} in 04_testing/")
            else:
                self.fail_check(f"Missing: {f}")

        # 05_review
        if Path("docs/05_review/PHASE3_ISSUES_INVENTORY.md").exists():
            self.pass_check("PHASE3_ISSUES_INVENTORY.md in 05_review/")
        else:
            self.warn_check("Missing: docs/05_review/PHASE3_ISSUES_INVENTORY.md")

    # ========================================================================
    # SECTION 3: FILE PLACEMENT RULES (Critical!)
    # ========================================================================
    def verify_placement_rules(self):
        self.section("3. FILE PLACEMENT RULES (Critical!)")

        # PHASE reviews should NOT be in planning
        bad_reviews = list(Path("docs/02_planning").glob("PHASE_*_REVIEW.md"))
        if bad_reviews:
            self.fail_check(f"PHASE reviews found in 02_planning/ (should be 05_review/)")
        else:
            self.pass_check("No PHASE reviews in 02_planning/ (correct)")

        # PHASE3_ISSUES should NOT be in testing
        if Path("docs/04_testing/PHASE3_ISSUES_INVENTORY.md").exists():
            self.fail_check("PHASE3_ISSUES in 04_testing/ (should be 05_review/)")
        else:
            self.pass_check("PHASE3_ISSUES not in 04_testing/ (correct)")

        # TECHNICAL_DECISIONS should be in 03_implementation
        if Path("docs/03_implementation/TECHNICAL_DECISIONS.md").exists():
            self.pass_check("TECHNICAL_DECISIONS.md in correct folder (03_implementation/)")
        else:
            self.fail_check("TECHNICAL_DECISIONS.md in wrong location")

    # ========================================================================
    # SECTION 4: REFERENCE INTEGRITY
    # ========================================================================
    def verify_references(self):
        self.section("4. REFERENCE INTEGRITY")

        bad_refs = []
        patterns = ["docs/technical/", "docs/testing/", "docs/planning/", "docs/input/", "docs/archive/"]

        for md_file in Path("docs").rglob("*.md"):
            content = md_file.read_text()
            for pattern in patterns:
                if pattern in content:
                    bad_refs.append(f"{md_file}: {pattern}")

        # Also check root files
        for root_file in ["README.md", "CONTRIBUTING.md"]:
            if Path(root_file).exists():
                content = Path(root_file).read_text()
                for pattern in patterns:
                    if pattern in content:
                        bad_refs.append(f"{root_file}: {pattern}")

        if bad_refs:
            self.fail_check(f"Found old-style doc references:")
            for ref in bad_refs[:5]:  # Show first 5
                print(f"    - {ref}")
            if len(bad_refs) > 5:
                print(f"    ... and {len(bad_refs) - 5} more")
        else:
            self.pass_check("No old-style doc references (all use docs/0X_/)")

    # ========================================================================
    # SECTION 5: WORKFLOW COHERENCE
    # ========================================================================
    def verify_workflow(self):
        self.section("5. WORKFLOW COHERENCE")

        workflow = {
            "01_input": ["02_planning"],
            "02_planning": ["01_input", "03_implementation"],
            "03_implementation": ["02_planning", "04_testing"],
            "04_testing": ["03_implementation", "05_review"],
            "05_review": ["04_testing", "06_release"],
            "06_release": ["05_review", "07_archive"],
            "07_archive": ["06_release"],
        }

        for folder, expected_refs in workflow.items():
            readme = Path(f"docs/{folder}/README.md")
            if readme.exists():
                content = readme.read_text()
                found_all = True
                for ref in expected_refs:
                    if f"docs/{ref}" not in content:
                        found_all = False
                        self.warn_check(f"{folder} README missing reference to docs/{ref}")

                if found_all:
                    self.pass_check(f"{folder} README has correct cross-references")

    # ========================================================================
    # SECTION 6: CONTENT QUALITY
    # ========================================================================
    def verify_content_quality(self):
        self.section("6. CONTENT QUALITY")

        # Check TODO.md exists
        if Path("docs/02_planning/TODO.md").exists():
            self.pass_check("TODO.md exists (source of truth)")
        else:
            self.fail_check("Missing: docs/02_planning/TODO.md")

        # Check archive is clean
        archive_files = list(Path("docs/07_archive").iterdir())
        archive_files = [f for f in archive_files if f.name not in ["README.md", ".gitkeep"]]
        if len(archive_files) == 0:
            self.pass_check("Archive is clean (only README.md)")
        else:
            self.warn_check(f"Archive contains {len(archive_files)} files (should be clean)")

    # ========================================================================
    # SECTION 7: OPTIONAL FILES
    # ========================================================================
    def verify_optional_files(self):
        self.section("7. OPTIONAL FILES TRACKING")

        optional = {
            "docs/05_review/REVIEW_DECISION.md": "Review decision",
            "docs/05_review/REVIEW_FEEDBACK.md": "Reviewer feedback",
            "docs/04_testing/TEST_PLAN.md": "Test documentation",
            "docs/06_release/UPDATED_SPEC.md": "Updated spec",
            "docs/06_release/RELEASE_NOTES.md": "Changelog",
        }

        for file, desc in optional.items():
            if Path(file).exists():
                self.pass_check(f"{Path(file).name} exists ({desc})")
            else:
                self.warn_check(f"{Path(file).name} not found ({desc} - optional)")

    # ========================================================================
    # SECTION 8: ROOT-LEVEL FILES
    # ========================================================================
    def verify_root_files(self):
        self.section("8. ROOT-LEVEL FILES")

        root_files = ["README.md", "CONTRIBUTING.md", ".githooks/pre-commit"]

        for file in root_files:
            if Path(file).exists():
                self.pass_check(f"{file} exists")
            else:
                self.fail_check(f"Missing: {file}")

    # ========================================================================
    # FINAL REPORT
    # ========================================================================
    def report(self):
        print("\n" + "=" * 60)
        print("VERIFICATION REPORT")
        print("=" * 60)
        print(f"\nChecks Passed: {self.passed}")
        print(f"Warnings:      {self.warnings}")
        print(f"Errors:        {self.errors}\n")

        if self.errors == 0:
            print("✓ READY FOR RELEASE")
            print("\nDocumentation is complete and coherent.")
            print("You can proceed with release/merge.")
            return 0
        else:
            print("✗ NOT READY FOR RELEASE")
            print(f"\nFix the {self.errors} error(s) above before proceeding.")
            return 1

    def run_all(self):
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║     DOCUMENTATION VERIFICATION - PRE-RELEASE CHECKLIST     ║")
        print("╚════════════════════════════════════════════════════════════╝")

        self.verify_structure()
        self.verify_file_placement()
        self.verify_placement_rules()
        self.verify_references()
        self.verify_workflow()
        self.verify_content_quality()
        self.verify_optional_files()
        self.verify_root_files()

        return self.report()


if __name__ == "__main__":
    verifier = DocVerifier()
    exit_code = verifier.run_all()
    sys.exit(exit_code)
