$base = 'C:\CreatorClipFactory'
$dirs = @(
    'core',
    'core\peakcut',
    'skills',
    'skills\video-editing-skills',
    'models',
    'config',
    'creators',
    'reference-library',
    'reference-library\incoming',
    'reference-library\styles',
    'reference-library\style-presets',
    'reference-library\analysis-cache',
    'reference-library\reference-metadata',
    'reference-library\version-history',
    'recordings',
    'rolling-buffer',
    'analysis',
    'highlights',
    'clips',
    'previews',
    'renders',
    'uploads',
    'database',
    'logs',
    'reports',
    'services',
    'workers',
    'dashboard',
    'dashboard\templates',
    'dashboard\static',
    'dashboard\static\css',
    'dashboard\static\js',
    'tests',
    'docs',
    'scripts',
    'tools',
    '.agents\skills'
)

foreach ($d in $dirs) {
    $full = Join-Path $base $d
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
    }
}

$agentSkillsDir = 'd:\factory\.agents\skills'
if (-not (Test-Path $agentSkillsDir)) {
    New-Item -ItemType Directory -Path $agentSkillsDir -Force | Out-Null
}

Write-Host "Directory tree initialized successfully at $base"
