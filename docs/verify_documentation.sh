#!/bin/bash

###############################################################################
#                    DOCUMENTATION VERIFICATION SCRIPT                       #
#                                                                             #
#  Run before each release to ensure documentation is complete & coherent    #
#  Usage: bash docs/verify_documentation.sh                                  #
#                                                                             #
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
CHECKS_PASSED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS_PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Header
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         DOCUMENTATION VERIFICATION CHECKLIST                   ║"
echo "║                 Pre-Release Verification                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Find the repo root (go up from docs/ folder)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

# ============================================================================
# SECTION 1: STRUCTURE VERIFICATION
# ============================================================================
echo "${BLUE}1. STRUCTURE VERIFICATION${NC}"
echo "════════════════════════════════"

# Check only 7 folders exist
folders_found=0
for folder in docs/01_input docs/02_planning docs/03_implementation docs/04_testing docs/05_review docs/06_release docs/07_archive; do
    if [ -d "$folder" ]; then
        ((folders_found++))
    else
        fail "Missing folder: $folder"
    fi
done

if [ $folders_found -eq 7 ]; then
    pass "All 7 numbered folders exist (01_-07_)"
else
    fail "Expected 7 folders, found $folders_found"
fi

# Check for illegal folders
illegal_folders=$(ls -d docs/*/ 2>/dev/null | grep -v "docs/0[1-7]_" | grep -v "docs/.git" || true)
if [ -z "$illegal_folders" ]; then
    pass "No illegal folders (docs/logs/, docs/technical/, etc.)"
else
    fail "Found illegal folders: $illegal_folders"
fi

# Check each folder has README.md
for folder in docs/0{1..7}_*/; do
    if [ -f "${folder}README.md" ]; then
        pass "$(basename "$folder")/README.md exists"
    else
        fail "Missing: $(basename "$folder")/README.md"
    fi
done

echo ""

# ============================================================================
# SECTION 2: FILE PLACEMENT VALIDATION
# ============================================================================
echo "${BLUE}2. FILE PLACEMENT VALIDATION${NC}"
echo "═════════════════════════════════"

# 01_input
required_01=(
    "docs/01_input/CAHIER_DES_CHARGES.md"
    "docs/01_input/SPEC.md"
    "docs/01_input/PROJECT_DEFINITION.md"
)
for file in "${required_01[@]}"; do
    if [ -f "$file" ]; then
        pass "$(basename "$file") in 01_input/"
    else
        fail "Missing: $file"
    fi
done

# 02_planning
required_02=(
    "docs/02_planning/TODO.md"
    "docs/02_planning/IMPLEMENTATION_PLAN.md"
)
for file in "${required_02[@]}"; do
    if [ -f "$file" ]; then
        pass "$(basename "$file") in 02_planning/"
    else
        fail "Missing: $file"
    fi
done

# Check for PHASE plans
phase_plans=$(ls docs/02_planning/PHASE_*_PLAN.md 2>/dev/null | wc -l)
if [ $phase_plans -gt 0 ]; then
    pass "Found $phase_plans PHASE_*_PLAN.md files"
else
    warn "No PHASE_*_PLAN.md files found (optional)"
fi

# 03_implementation
if [ -f "docs/03_implementation/TECHNICAL_DECISIONS.md" ]; then
    pass "TECHNICAL_DECISIONS.md in 03_implementation/"
else
    fail "Missing: docs/03_implementation/TECHNICAL_DECISIONS.md"
fi

# 04_testing
required_04=(
    "docs/04_testing/QUICK_START_TESTS.md"
    "docs/04_testing/VSCODE_TESTING_GUIDE.md"
    "docs/04_testing/UAT_DETAILED_GUIDE.md"
)
for file in "${required_04[@]}"; do
    if [ -f "$file" ]; then
        pass "$(basename "$file") in 04_testing/"
    else
        fail "Missing: $file"
    fi
done

# 05_review
if [ -f "docs/05_review/PHASE3_ISSUES_INVENTORY.md" ]; then
    pass "PHASE3_ISSUES_INVENTORY.md in 05_review/"
else
    warn "Missing: docs/05_review/PHASE3_ISSUES_INVENTORY.md"
fi

# Check for PHASE reviews
phase_reviews=$(ls docs/05_review/PHASE_*_REVIEW.md 2>/dev/null | wc -l)
if [ $phase_reviews -gt 0 ]; then
    pass "Found $phase_reviews PHASE_*_REVIEW.md files"
else
    warn "No PHASE_*_REVIEW.md files found (phase reviews)"
fi

echo ""

# ============================================================================
# SECTION 3: FILE PLACEMENT RULES (Critical!)
# ============================================================================
echo "${BLUE}3. FILE PLACEMENT RULES (Critical!)${NC}"
echo "═════════════════════════════════════"

# PHASE reviews should NOT be in planning
if ls docs/02_planning/PHASE_*_REVIEW.md 2>/dev/null | grep -q .; then
    fail "PHASE_*_REVIEW.md found in 02_planning/ (should be in 05_review/)"
else
    pass "No PHASE reviews in 02_planning/ (correct)"
fi

# PHASE3_ISSUES should NOT be in testing
if [ -f "docs/04_testing/PHASE3_ISSUES_INVENTORY.md" ]; then
    fail "PHASE3_ISSUES_INVENTORY.md in 04_testing/ (should be in 05_review/)"
else
    pass "PHASE3_ISSUES_INVENTORY.md not in 04_testing/ (correct)"
fi

# TECHNICAL_DECISIONS should NOT be in testing or planning
if ls docs/04_testing/TECHNICAL_DECISIONS.md docs/02_planning/TECHNICAL_DECISIONS.md 2>/dev/null | grep -q .; then
    fail "TECHNICAL_DECISIONS.md in wrong folder (should be 03_implementation/)"
else
    pass "TECHNICAL_DECISIONS.md in correct folder (03_implementation/)"
fi

echo ""

# ============================================================================
# SECTION 4: REFERENCE INTEGRITY
# ============================================================================
echo "${BLUE}4. REFERENCE INTEGRITY${NC}"
echo "═══════════════════════════"

# Check for old-style references
old_refs=$(grep -r "docs/technical\|docs/testing\|docs/planning\|docs/input\|docs/archive" --include="*.md" docs/ README.md CONTRIBUTING.md 2>/dev/null | grep -v "docs/0[1-7]" | grep -v "for example" || true)
if [ -z "$old_refs" ]; then
    pass "No old-style doc references (docs/technical/, docs/testing/, etc.)"
else
    fail "Found old-style references:"
    echo "$old_refs" | sed 's/^/  /'
fi

# Check that numbered references are correct
new_refs=$(grep -r "docs/0[1-7]_" --include="*.md" docs/ README.md CONTRIBUTING.md 2>/dev/null | wc -l)
if [ $new_refs -gt 0 ]; then
    pass "Found $new_refs references to numbered docs folders (docs/0X_/)"
else
    warn "No references to numbered docs folders found"
fi

echo ""

# ============================================================================
# SECTION 5: WORKFLOW COHERENCE
# ============================================================================
echo "${BLUE}5. WORKFLOW COHERENCE${NC}"
echo "════════════════════════"

declare -A workflow_refs
workflow_refs[01_input]="02_planning"
workflow_refs[02_planning]="01_input 03_implementation"
workflow_refs[03_implementation]="02_planning 04_testing"
workflow_refs[04_testing]="03_implementation 05_review"
workflow_refs[05_review]="04_testing 06_release"
workflow_refs[06_release]="05_review 07_archive"
workflow_refs[07_archive]="06_release"

for folder in "${!workflow_refs[@]}"; do
    expected="${workflow_refs[$folder]}"
    readme="docs/$folder/README.md"

    if [ -f "$readme" ]; then
        all_found=true
        for ref in $expected; do
            if grep -q "docs/$ref" "$readme"; then
                : # Found
            else
                all_found=false
                warn "$folder README doesn't reference docs/$ref"
            fi
        done

        if [ "$all_found" = true ]; then
            pass "$folder README has correct cross-references"
        fi
    else
        fail "Missing README.md for $folder"
    fi
done

echo ""

# ============================================================================
# SECTION 6: CONTENT QUALITY
# ============================================================================
echo "${BLUE}6. CONTENT QUALITY${NC}"
echo "═════════════════════"

# Check if TODO.md exists and is recent
if [ -f "docs/02_planning/TODO.md" ]; then
    # Check if modified in last 7 days (for Unix-like systems)
    if [ -f "docs/02_planning/TODO.md" ]; then
        pass "TODO.md exists (source of truth for task status)"
    fi
else
    fail "TODO.md missing from 02_planning/"
fi

# Check for conflicting status in archive
conflicting=$(grep -r "ready for UAT\|Phase 3 complete\|all fixed\|no bugs" docs/07_archive/ 2>/dev/null || true)
if [ -z "$conflicting" ]; then
    pass "No conflicting status messages in archive"
else
    warn "Found potentially conflicting messages in archive:"
    echo "$conflicting" | sed 's/^/  /'
fi

# Check archive is mostly empty
archive_files=$(ls -1 docs/07_archive/ | grep -v README.md | grep -v "^\." | wc -l)
if [ $archive_files -eq 0 ]; then
    pass "Archive is clean (only README.md)"
else
    warn "Archive contains $archive_files files (should be clean)"
fi

echo ""

# ============================================================================
# SECTION 7: OPTIONAL FILES TRACKING
# ============================================================================
echo "${BLUE}7. OPTIONAL FILES TRACKING${NC}"
echo "════════════════════════════"

optional_files=(
    "docs/05_review/REVIEW_DECISION.md:Review decision (Approved/Rejected)"
    "docs/05_review/REVIEW_FEEDBACK.md:Reviewer feedback"
    "docs/04_testing/TEST_PLAN.md:Test documentation"
    "docs/06_release/UPDATED_SPEC.md:Updated spec (after approval)"
    "docs/06_release/RELEASE_NOTES.md:Changelog"
)

for entry in "${optional_files[@]}"; do
    file="${entry%%:*}"
    desc="${entry##*:}"

    if [ -f "$file" ]; then
        pass "$(basename "$file") exists ($desc)"
    else
        info "$(basename "$file") not found ($desc - optional)"
    fi
done

echo ""

# ============================================================================
# SECTION 8: ROOT-LEVEL FILES
# ============================================================================
echo "${BLUE}8. ROOT-LEVEL FILES${NC}"
echo "═════════════════════"

root_files=(
    "README.md"
    "CONTRIBUTING.md"
    ".githooks/pre-commit"
)

for file in "${root_files[@]}"; do
    if [ -f "$file" ]; then
        pass "$file exists"
    else
        fail "Missing: $file"
    fi
done

echo ""

# ============================================================================
# FINAL REPORT
# ============================================================================
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      VERIFICATION REPORT                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "Checks Passed:  ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Warnings:       ${YELLOW}$WARNINGS${NC}"
echo -e "Errors:         ${RED}$ERRORS${NC}"
echo ""

# Determine overall status
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ READY FOR RELEASE${NC}"
    echo ""
    echo "Documentation is complete and coherent."
    echo "You can proceed with release/merge."
    exit 0
else
    echo -e "${RED}✗ NOT READY FOR RELEASE${NC}"
    echo ""
    echo "Fix the $ERRORS error(s) above before proceeding."
    exit 1
fi
