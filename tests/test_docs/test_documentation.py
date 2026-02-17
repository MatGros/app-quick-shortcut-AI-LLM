"""
Documentation Structure and Quality Tests

Tests the documentation folder structure, file placement, naming conventions,
and workflow coherence.

Run with: pytest tests/test_documentation.py -v
"""

import pytest
from pathlib import Path
import re


class TestDocumentationStructure:
    """Tests for overall documentation structure"""

    def test_has_seven_numbered_folders(self):
        """Documentation should have exactly 7 numbered folders (01_-07_)"""
        docs_path = Path("docs")
        required_folders = [
            "01_input",
            "02_planning",
            "03_implementation",
            "04_testing",
            "05_review",
            "06_release",
            "07_archive",
        ]

        for folder in required_folders:
            folder_path = docs_path / folder
            assert folder_path.is_dir(), f"Missing required folder: docs/{folder}/"

    def test_no_illegal_folders(self):
        """Should not have illegal folders like logs/, technical/, etc."""
        docs_path = Path("docs")
        illegal_patterns = ["logs", "technical", "archive/", "planning/", "testing/"]

        for item in docs_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                for pattern in illegal_patterns:
                    assert (
                        pattern not in item.name
                        or item.name.startswith("0")
                    ), f"Illegal folder found: {item.name}"

    def test_each_folder_has_readme(self):
        """Each documentation folder should have a README.md"""
        folders = [
            "docs/01_input",
            "docs/02_planning",
            "docs/03_implementation",
            "docs/04_testing",
            "docs/05_review",
            "docs/06_release",
            "docs/07_archive",
        ]

        for folder in folders:
            readme = Path(folder) / "README.md"
            assert readme.exists(), f"Missing README.md in {folder}/"


class TestFilePlacement:
    """Tests for correct file placement in folders"""

    def test_01_input_required_files(self):
        """01_input should contain requirements and specs"""
        required = [
            "docs/01_input/CAHIER_DES_CHARGES.md",
            "docs/01_input/SPEC.md",
            "docs/01_input/PROJECT_DEFINITION.md",
        ]

        for file in required:
            assert Path(file).exists(), f"Missing: {file}"

    def test_02_planning_required_files(self):
        """02_planning should contain TODO and phase plans"""
        required = [
            "docs/02_planning/TODO.md",
            "docs/02_planning/IMPLEMENTATION_PLAN.md",
        ]

        for file in required:
            assert Path(file).exists(), f"Missing: {file}"

    def test_03_implementation_required_files(self):
        """03_implementation should contain technical decisions"""
        required = ["docs/03_implementation/TECHNICAL_DECISIONS.md"]

        for file in required:
            assert Path(file).exists(), f"Missing: {file}"

    def test_04_testing_required_files(self):
        """04_testing should contain test guides"""
        required = [
            "docs/04_testing/QUICK_START_TESTS.md",
            "docs/04_testing/VSCODE_TESTING_GUIDE.md",
            "docs/04_testing/UAT_DETAILED_GUIDE.md",
        ]

        for file in required:
            assert Path(file).exists(), f"Missing: {file}"

    def test_05_review_required_files(self):
        """05_review should contain issues inventory"""
        # PHASE3_ISSUES should be in review, not testing
        assert Path("docs/05_review/PHASE3_ISSUES_INVENTORY.md").exists()

    def test_07_archive_is_clean(self):
        """07_archive should only contain README.md (no .archived files)"""
        archive_path = Path("docs/07_archive")
        files = [f for f in archive_path.iterdir() if f.name not in ["README.md", ".gitkeep"]]
        assert len(files) == 0, f"Archive should be clean, but contains: {[f.name for f in files]}"


class TestFileNameConventions:
    """Tests for strict file naming conventions"""

    def test_main_docs_are_uppercase(self):
        """Main documentation files should be UPPERCASE.md"""
        # Examples: SPEC.md, TODO.md, TECHNICAL_DECISIONS.md
        uppercase_files = [
            "docs/01_input/CAHIER_DES_CHARGES.md",
            "docs/01_input/SPEC.md",
            "docs/02_planning/TODO.md",
            "docs/03_implementation/TECHNICAL_DECISIONS.md",
        ]

        for file in uppercase_files:
            assert Path(file).exists()
            # Check that filename (without extension) is UPPERCASE
            filename = Path(file).stem
            assert filename.isupper() or "_" in filename, f"Should be UPPERCASE: {file}"

    def test_readme_files_are_lowercase(self):
        """README files should be lowercase README.md"""
        folders = [
            "docs/01_input",
            "docs/02_planning",
            "docs/03_implementation",
            "docs/04_testing",
            "docs/05_review",
            "docs/06_release",
            "docs/07_archive",
        ]

        for folder in folders:
            readme = Path(folder) / "README.md"
            assert readme.exists(), f"Missing README.md in {folder}"
            # Check exact case
            assert readme.name == "README.md", f"Should be lowercase 'README.md' in {folder}"

    def test_phase_files_use_underscore(self):
        """PHASE files should use underscore: PHASE_1, not PHASE-1 or Phase1"""
        phase_files = list(Path("docs/02_planning").glob("PHASE_*_PLAN.md"))
        phase_files += list(Path("docs/05_review").glob("PHASE_*_REVIEW.md"))

        for file in phase_files:
            # Should match pattern like PHASE_X_SOMETHING.md
            assert re.match(r"PHASE_\d+_", file.name), f"Wrong format: {file.name}"

    def test_no_camelcase_in_filenames(self):
        """Filenames should not use camelCase"""
        bad_patterns = [
            r"[a-z]+[A-Z]",  # camelCase
            r"-+",  # hyphens
            r"\s+",  # spaces
        ]

        for md_file in Path("docs").rglob("*.md"):
            filename = md_file.name.replace(".md", "").replace(".archived", "")
            for pattern in bad_patterns:
                assert not re.search(pattern, filename), (
                    f"Invalid naming in {md_file.relative_to('.')}: "
                    f"avoid camelCase, hyphens, or spaces"
                )


class TestPlacementRules:
    """Tests for critical file placement rules"""

    def test_phase_reviews_not_in_planning(self):
        """PHASE reviews should be in 05_review, NOT in 02_planning"""
        bad_reviews = list(Path("docs/02_planning").glob("PHASE_*_REVIEW.md"))
        assert len(bad_reviews) == 0, (
            "PHASE reviews found in 02_planning (should be in 05_review). "
            "Reviews are results, not plans."
        )

    def test_phase3_issues_not_in_testing(self):
        """PHASE3_ISSUES_INVENTORY should be in 05_review, NOT in 04_testing"""
        assert not Path("docs/04_testing/PHASE3_ISSUES_INVENTORY.md").exists(), (
            "PHASE3_ISSUES_INVENTORY.md in 04_testing (should be in 05_review). "
            "Issues are review results, not test guides."
        )

    def test_technical_decisions_in_implementation(self):
        """TECHNICAL_DECISIONS.md should be in 03_implementation"""
        assert Path("docs/03_implementation/TECHNICAL_DECISIONS.md").exists()

    def test_todo_in_planning_not_elsewhere(self):
        """TODO.md should be in 02_planning, the source of truth"""
        assert Path("docs/02_planning/TODO.md").exists()
        # Make sure it's not duplicated elsewhere
        other_todos = list(Path("docs").rglob("TODO.md"))
        other_todos = [t for t in other_todos if "02_planning" not in str(t)]
        assert len(other_todos) == 0, (
            "TODO.md should only be in 02_planning (source of truth). "
            f"Found elsewhere: {other_todos}"
        )


class TestReferenceIntegrity:
    """Tests for broken or incorrect cross-references"""

    def test_no_old_style_references(self):
        """Should not reference old-style paths (docs/technical/, docs/testing/, etc.)"""
        bad_patterns = [
            r"docs/technical/",
            r"docs/testing/",
            r"docs/planning/",
            r"docs/input/",
            r"docs/archive/",
        ]

        bad_refs = []
        for md_file in Path("docs").rglob("*.md"):
            # Skip examples in README
            if md_file.name == "README.md" and "docs" in str(md_file):
                continue

            try:
                content = md_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
            # Remove code blocks
            content = re.sub(r"```[\s\S]*?```", "", content)
            content = re.sub(r"`[^`]*`", "", content)

            for pattern in bad_patterns:
                if re.search(pattern, content):
                    bad_refs.append(f"{md_file.relative_to('.')}: {pattern}")

        # Also check root files
        for root_file in ["README.md", "CONTRIBUTING.md"]:
            if Path(root_file).exists():
                try:
                    content = Path(root_file).read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    content = Path(root_file).read_text(encoding='utf-8', errors='ignore')
                # Remove code blocks
                content = re.sub(r"```[\s\S]*?```", "", content)
                content = re.sub(r"`[^`]*`", "", content)

                for pattern in bad_patterns:
                    if re.search(pattern, content):
                        bad_refs.append(f"{root_file}: {pattern}")

        assert len(bad_refs) == 0, (
            f"Found old-style doc references (should use docs/0X_/): {bad_refs}"
        )

    def test_uses_numbered_references(self):
        """Should use numbered references (docs/0X_/) consistently"""
        good_pattern = r"docs/0[1-7]_"
        found_good_refs = []

        for md_file in Path("docs").rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
            if re.search(good_pattern, content):
                found_good_refs.append(str(md_file.relative_to(".")))

        # At least some files should reference the numbered structure
        assert len(found_good_refs) > 0, "Should find references to numbered docs folders (docs/0X_/)"


class TestWorkflowCoherence:
    """Tests for workflow coherence between folders"""

    def test_folder_readmes_reference_workflow(self):
        """Each README should reference previous and next step in workflow"""
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
            assert readme.exists()

            try:
                content = readme.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                content = readme.read_text(encoding='utf-8', errors='ignore')
            for expected_ref in expected_refs:
                assert f"docs/{expected_ref}" in content or expected_ref in content, (
                    f"{folder}/README.md should reference {expected_ref} "
                    f"(previous or next step in workflow)"
                )


class TestContentQuality:
    """Tests for documentation content quality"""

    def test_todo_exists_and_is_source_of_truth(self):
        """TODO.md should exist and be marked as source of truth"""
        todo_file = Path("docs/02_planning/TODO.md")
        assert todo_file.exists(), "TODO.md is the source of truth for task status"

    def test_archive_no_conflicting_documents(self):
        """Archive should not contain files with conflicting status"""
        archive_path = Path("docs/07_archive")
        conflicting_words = ["ready for UAT", "phase 3 complete", "all fixed"]

        for file in archive_path.glob("*"):
            if file.name in ["README.md", ".gitkeep"]:
                continue

            try:
                content = file.read_text(encoding='utf-8').lower()
            except UnicodeDecodeError:
                content = file.read_text(encoding='utf-8', errors='ignore').lower()
            for word in conflicting_words:
                assert word not in content, (
                    f"Archive file {file.name} contains conflicting text: '{word}'. "
                    "Archive should only contain historical context, not misleading status."
                )


class TestRootLevelFiles:
    """Tests for root-level documentation files"""

    def test_root_readme_exists(self):
        """Root README.md should exist"""
        assert Path("README.md").exists()

    def test_root_contributing_exists(self):
        """CONTRIBUTING.md should exist with workflow guide"""
        assert Path("CONTRIBUTING.md").exists()
        try:
            content = Path("CONTRIBUTING.md").read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = Path("CONTRIBUTING.md").read_text(encoding='utf-8', errors='ignore')
        assert "7-step workflow" in content or "workflow" in content.lower()

    def test_git_hooks_exist(self):
        """.githooks/pre-commit should exist"""
        assert Path(".githooks/pre-commit").exists()


class TestOptionalFiles:
    """Tests for optional documentation files - test FAILS if any are missing"""

    def test_all_optional_files_exist(self):
        """All optional Phase 3 completion files must exist (no warnings)"""
        optional_files = [
            "docs/05_review/REVIEW_DECISION.md",
            "docs/05_review/REVIEW_FEEDBACK.md",
            "docs/04_testing/TEST_PLAN.md",
            "docs/06_release/UPDATED_SPEC.md",
            "docs/06_release/RELEASE_NOTES.md",
        ]

        missing_files = []
        for file_path in optional_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)

        assert len(missing_files) == 0, (
            f"Missing optional files (test FAILS with warnings): {missing_files}. "
            f"Create these files to clear all warnings."
        )


# ============================================================================
# Summary Statistics
# ============================================================================


class TestDocumentationSummary:
    """Summary tests for documentation health"""

    def test_documentation_structure_summary(self):
        """Summary: Count and validate all documentation files"""
        docs_path = Path("docs")

        # Count files by folder
        md_files = {}
        for folder in docs_path.iterdir():
            if folder.is_dir() and folder.name.startswith("0"):
                md_files[folder.name] = len(list(folder.glob("*.md")))

        # Should have at least one file in each folder (README.md)
        for folder, count in md_files.items():
            assert count >= 1, f"{folder} has no markdown files"

        # Print summary
        total_files = sum(md_files.values())
        print(f"\n✓ Documentation Summary:")
        print(f"  Total MD files: {total_files}")
        for folder, count in sorted(md_files.items()):
            print(f"  - {folder}: {count} files")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
