# Documentation Verification Script - Pre-Release Checklist
#
# Run before each release to ensure documentation is complete and coherent.
#
# Usage:
#   .\docs\verify_docs.ps1
#   or from root: powershell -ExecutionPolicy Bypass -File docs\verify_docs.ps1

param(
    [switch]$Detailed = $false
)

# Colors
$colors = @{
    Pass   = [System.ConsoleColor]::Green
    Warn   = [System.ConsoleColor]::Yellow
    Error  = [System.ConsoleColor]::Red
    Info   = [System.ConsoleColor]::Cyan
    Normal = [System.ConsoleColor]::White
}

# Counters
$script:passed = 0
$script:warnings = 0
$script:errors = 0

# Helper functions
function Write-Pass {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor $colors.Pass
    $script:passed++
}

function Write-Warn {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor $colors.Warn
    $script:warnings++
}

function Write-Fail {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor $colors.Error
    $script:errors++
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host $Title -ForegroundColor $colors.Info
    Write-Host ("=" * 60) -ForegroundColor $colors.Info
}

# ============================================================================
# SECTION 1: STRUCTURE VERIFICATION
# ============================================================================
function Test-Structure {
    Write-Section "1. STRUCTURE VERIFICATION"

    $requiredFolders = @(
        "docs\01_input",
        "docs\02_planning",
        "docs\03_implementation",
        "docs\04_testing",
        "docs\05_review",
        "docs\06_release",
        "docs\07_archive"
    )

    # Check all 7 folders exist
    foreach ($folder in $requiredFolders) {
        if (Test-Path -Path $folder -PathType Container) {
            Write-Pass "$folder\ exists"
        } else {
            Write-Fail "Missing: $folder\"
        }
    }

    # Check no illegal folders
    $illegalFolders = Get-ChildItem "docs" -Directory | Where-Object {
        $_.Name -notmatch "^0[1-7]_" -and $_.Name -notlike ".git*"
    }

    if ($illegalFolders.Count -eq 0) {
        Write-Pass "No illegal folders (no docs\logs\, docs\technical\, etc.)"
    } else {
        Write-Fail "Illegal folders found: $($illegalFolders.Name -join ', ')"
    }

    # Check each folder has README.md
    foreach ($folder in $requiredFolders) {
        $readme = Join-Path $folder "README.md"
        if (Test-Path -Path $readme) {
            Write-Pass "$folder\README.md exists"
        } else {
            Write-Fail "Missing: $readme"
        }
    }
}

# ============================================================================
# SECTION 2: FILE PLACEMENT VALIDATION
# ============================================================================
function Test-FilePlacement {
    Write-Section "2. FILE PLACEMENT VALIDATION"

    # 01_input required files
    $inputFiles = @(
        "docs\01_input\CAHIER_DES_CHARGES.md",
        "docs\01_input\SPEC.md",
        "docs\01_input\PROJECT_DEFINITION.md"
    )

    foreach ($file in $inputFiles) {
        if (Test-Path -Path $file) {
            Write-Pass "$(Split-Path $file -Leaf) in 01_input\"
        } else {
            Write-Fail "Missing: $file"
        }
    }

    # 02_planning required files
    $planningFiles = @(
        "docs\02_planning\TODO.md",
        "docs\02_planning\IMPLEMENTATION_PLAN.md"
    )

    foreach ($file in $planningFiles) {
        if (Test-Path -Path $file) {
            Write-Pass "$(Split-Path $file -Leaf) in 02_planning\"
        } else {
            Write-Fail "Missing: $file"
        }
    }

    # 03_implementation
    if (Test-Path -Path "docs\03_implementation\TECHNICAL_DECISIONS.md") {
        Write-Pass "TECHNICAL_DECISIONS.md in 03_implementation\"
    } else {
        Write-Fail "Missing: docs\03_implementation\TECHNICAL_DECISIONS.md"
    }

    # 04_testing required files
    $testingFiles = @(
        "docs\04_testing\QUICK_START_TESTS.md",
        "docs\04_testing\VSCODE_TESTING_GUIDE.md",
        "docs\04_testing\UAT_DETAILED_GUIDE.md"
    )

    foreach ($file in $testingFiles) {
        if (Test-Path -Path $file) {
            Write-Pass "$(Split-Path $file -Leaf) in 04_testing\"
        } else {
            Write-Fail "Missing: $file"
        }
    }

    # 05_review
    if (Test-Path -Path "docs\05_review\PHASE3_ISSUES_INVENTORY.md") {
        Write-Pass "PHASE3_ISSUES_INVENTORY.md in 05_review\"
    } else {
        Write-Warn "Missing: docs\05_review\PHASE3_ISSUES_INVENTORY.md"
    }
}

# ============================================================================
# SECTION 3: FILE PLACEMENT RULES (Critical!)
# ============================================================================
function Test-PlacementRules {
    Write-Section "3. FILE PLACEMENT RULES (Critical!)"

    # PHASE reviews should NOT be in planning
    $badReviews = Get-ChildItem "docs\02_planning\PHASE_*_REVIEW.md" -ErrorAction SilentlyContinue
    if ($badReviews) {
        Write-Fail "PHASE reviews found in 02_planning\ (should be 05_review\)"
    } else {
        Write-Pass "No PHASE reviews in 02_planning\ (correct)"
    }

    # PHASE3_ISSUES should NOT be in testing
    if (Test-Path -Path "docs\04_testing\PHASE3_ISSUES_INVENTORY.md") {
        Write-Fail "PHASE3_ISSUES in 04_testing\ (should be 05_review\)"
    } else {
        Write-Pass "PHASE3_ISSUES not in 04_testing\ (correct)"
    }

    # TECHNICAL_DECISIONS should be in 03_implementation
    if (Test-Path -Path "docs\03_implementation\TECHNICAL_DECISIONS.md") {
        Write-Pass "TECHNICAL_DECISIONS.md in correct folder (03_implementation\)"
    } else {
        Write-Fail "TECHNICAL_DECISIONS.md in wrong location"
    }
}

# ============================================================================
# SECTION 4: REFERENCE INTEGRITY
# ============================================================================
function Test-References {
    Write-Section "4. REFERENCE INTEGRITY"

    $badPatterns = @("docs/technical/", "docs/testing/", "docs/planning/", "docs/input/", "docs/archive/")
    $badRefs = @()

    # Helper to remove code blocks from content
    function Remove-CodeBlocks {
        param([string]$Content)
        # Remove markdown code blocks (```)
        $Content = $Content -replace '```[\s\S]*?```', ''
        # Remove inline code (`)
        $Content = $Content -replace '`[^`]*`', ''
        return $Content
    }

    # Check docs folder (excluding README which has examples)
    Get-ChildItem "docs" -Recurse -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $content = Remove-CodeBlocks -Content $content
        foreach ($pattern in $badPatterns) {
            if ($content -match [regex]::Escape($pattern)) {
                $badRefs += "$($_.FullName): $pattern"
            }
        }
    }

    # Check root files (skip docs/README.md as it has examples)
    foreach ($file in @("README.md", "CONTRIBUTING.md")) {
        if (Test-Path -Path $file) {
            $content = Get-Content $file -Raw
            $content = Remove-CodeBlocks -Content $content
            foreach ($pattern in $badPatterns) {
                if ($content -match [regex]::Escape($pattern)) {
                    $badRefs += "$file`: $pattern"
                }
            }
        }
    }

    if ($badRefs.Count -gt 0) {
        Write-Fail "Found old-style doc references:"
        $badRefs | Select-Object -First 5 | ForEach-Object { Write-Host "    - $_" }
        if ($badRefs.Count -gt 5) {
            Write-Host "    ... and $($badRefs.Count - 5) more"
        }
    } else {
        Write-Pass "No old-style doc references (all use docs/0X_/)"
    }
}

# ============================================================================
# SECTION 5: WORKFLOW COHERENCE
# ============================================================================
function Test-Workflow {
    Write-Section "5. WORKFLOW COHERENCE"

    $workflow = @{
        "01_input" = @("02_planning")
        "02_planning" = @("01_input", "03_implementation")
        "03_implementation" = @("02_planning", "04_testing")
        "04_testing" = @("03_implementation", "05_review")
        "05_review" = @("04_testing", "06_release")
        "06_release" = @("05_review", "07_archive")
        "07_archive" = @("06_release")
    }

    foreach ($folder in $workflow.Keys) {
        $readme = "docs\$folder\README.md"
        if (Test-Path -Path $readme) {
            $content = Get-Content $readme -Raw
            $foundAll = $true
            foreach ($ref in $workflow[$folder]) {
                if ($content -notmatch "docs/$ref") {
                    Write-Warn "$folder README missing reference to docs/$ref"
                    $foundAll = $false
                }
            }
            if ($foundAll) {
                Write-Pass "$folder README has correct cross-references"
            }
        }
    }
}

# ============================================================================
# SECTION 6: CONTENT QUALITY
# ============================================================================
function Test-ContentQuality {
    Write-Section "6. CONTENT QUALITY"

    # Check TODO.md exists
    if (Test-Path -Path "docs\02_planning\TODO.md") {
        Write-Pass "TODO.md exists (source of truth)"
    } else {
        Write-Fail "Missing: docs\02_planning\TODO.md"
    }

    # Check archive is clean
    $archiveFiles = Get-ChildItem "docs\07_archive" | Where-Object {
        $_.Name -ne "README.md" -and $_.Name -ne ".gitkeep"
    }

    if ($archiveFiles.Count -eq 0) {
        Write-Pass "Archive is clean (only README.md)"
    } else {
        Write-Warn "Archive contains $($archiveFiles.Count) files (should be clean)"
    }
}

# ============================================================================
# SECTION 7: OPTIONAL FILES
# ============================================================================
function Test-OptionalFiles {
    Write-Section "7. OPTIONAL FILES TRACKING"

    $optional = @{
        "docs\05_review\REVIEW_DECISION.md" = "Review decision"
        "docs\05_review\REVIEW_FEEDBACK.md" = "Reviewer feedback"
        "docs\04_testing\TEST_PLAN.md" = "Test documentation"
        "docs\06_release\UPDATED_SPEC.md" = "Updated spec"
        "docs\06_release\RELEASE_NOTES.md" = "Changelog"
    }

    foreach ($file in $optional.Keys) {
        $desc = $optional[$file]
        $name = Split-Path $file -Leaf
        if (Test-Path -Path $file) {
            Write-Pass "$name exists ($desc)"
        } else {
            Write-Warn "$name not found ($desc - optional)"
        }
    }
}

# ============================================================================
# SECTION 8: ROOT-LEVEL FILES
# ============================================================================
function Test-RootFiles {
    Write-Section "8. ROOT-LEVEL FILES"

    $rootFiles = @("README.md", "CONTRIBUTING.md", ".githooks\pre-commit")

    foreach ($file in $rootFiles) {
        if (Test-Path -Path $file) {
            Write-Pass "$file exists"
        } else {
            Write-Fail "Missing: $file"
        }
    }
}

# ============================================================================
# FINAL REPORT
# ============================================================================
function Write-Report {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor $colors.Info
    Write-Host "VERIFICATION REPORT" -ForegroundColor $colors.Info
    Write-Host ("=" * 60) -ForegroundColor $colors.Info
    Write-Host ""
    Write-Host "Checks Passed: " -NoNewline
    Write-Host $script:passed -ForegroundColor $colors.Pass
    Write-Host "Warnings:      " -NoNewline
    Write-Host $script:warnings -ForegroundColor $colors.Warn
    Write-Host "Errors:        " -NoNewline
    Write-Host $script:errors -ForegroundColor $colors.Error
    Write-Host ""

    if ($script:errors -eq 0) {
        Write-Host "✓ READY FOR RELEASE" -ForegroundColor $colors.Pass
        Write-Host ""
        Write-Host "Documentation is complete and coherent."
        Write-Host "You can proceed with release/merge."
        return 0
    } else {
        Write-Host "✗ NOT READY FOR RELEASE" -ForegroundColor $colors.Error
        Write-Host ""
        Write-Host "Fix the $($script:errors) error(s) above before proceeding." -ForegroundColor $colors.Error
        return 1
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Print header
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor $colors.Info
Write-Host "║  DOCUMENTATION VERIFICATION - PRE-RELEASE CHECKLIST        ║" -ForegroundColor $colors.Info
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor $colors.Info

# Run all tests
Test-Structure
Test-FilePlacement
Test-PlacementRules
Test-References
Test-Workflow
Test-ContentQuality
Test-OptionalFiles
Test-RootFiles

# Print report and exit
$exitCode = Write-Report
exit $exitCode
