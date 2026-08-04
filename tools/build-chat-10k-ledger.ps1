param(
  [string]$ChatPath = 'C:\Users\USER\Downloads\qwen\chat-Belentani 10.00 Website Modules.txt',
  [string]$RepoPath = 'C:\Users\USER\Desktop\belentani_Omega-live'
)

$ErrorActionPreference = 'Stop'
$raw = Get-Content -LiteralPath $ChatPath -Raw -Encoding UTF8
$lines = $raw -split "\r?\n"
$records = [System.Collections.Generic.List[object]]::new()
$seen = @{}

$modules = @(
  'Identidad','Lore/Códice','Sonido','Archivo visual','Gamificación','Studio IA','Neural chat','Frecuencias','Multiverso Zion','Judas/antagonista',
  'Llave dorada','Cinco elementos','Motor OMEGA','Discografía','Live/eventos','Newsletter','Social','PWA/móvil','Accesibilidad','SEO','Analítica','Seguridad',
  'API','Monetización','Colaboraciones','Press/EPK','Blog Crónica','Letras','Motor de audio','Personalización','XR','Educación','Archivo/cápsulas','i18n',
  'Legal/ética IA','Performance','Ecosistema dominios','Comunidad externa','Sostenibilidad','OMEGA/escatología'
)
$mechanics = @(
  'Colección/álbum','Reto diario','Votación comunitaria','Remix/mashup','Gate temporal','Geolocalización','Realidad aumentada','IA generativa texto',
  'IA generativa imagen','IA generativa audio','Ramificación narrativa','Telemetría/HUD en vivo','Código secreto/easter egg','XP/leaderboard',
  'Contenido generado por usuario','Curaduría/jurado','Suscripción/tier','Sorteo/recompensa','Test/quiz','Canvas colaborativo','Chat con persona',
  'Transmisión de voz','Visualización de datos','API/integración tercera','Puente físico-digital'
)
$cores = @('Judas','Llave dorada','Zion/multiverso','Cinco elementos','Frecuencias 432–852','El Entre','Traición/beso','Sanación/hackeo','Seis discos','Motor OMEGA')
$channels = @('belentani.es','buildai.space','Instagram','TikTok','YouTube','Spotify/SoundCloud/Deezer','Discord','Telegram','Email/newsletter','Live')

function Get-Target([int]$module) {
  if($module -le 8){ return 'js/08-content.js + data/canon.json' }
  if($module -le 12){ return 'js/06-ai.js + js/07-portal.js' }
  if($module -eq 13){ return 'js/03-webgl.js + site/js/core/edition-engine.js' }
  if($module -le 18){ return 'index.html + js/05-audio.js' }
  if($module -le 22){ return 'index.html + css/main.css + sw.js' }
  if($module -le 25){ return 'server/API boundary; local adapter only' }
  if($module -le 29){ return 'index.html + js/06-ai.js + js/08-content.js' }
  if($module -le 35){ return 'site/js/core/edition-engine.js + data/canon.json' }
  return 'tools + docs + runtime performance gates'
}

function Add-Record($record) {
  $id = [int]$record.id
  if(-not $seen.ContainsKey($id)) { $seen[$id] = $true; $records.Add([pscustomobject]$record) }
}

# 001–300: ideas explicitly written in the chat, overlaid on the matrix.
$explicitByGrid = @{}
$explicitCount = 0
$explicit = [regex]::Matches($raw, '\*\*(\d{3})\*\*\s+(.+?)(?=\s+\*\*\d{3}\*\*|\r?\n|$)')
foreach($m in $explicit) {
  $chatNumber = [int]$m.Groups[1].Value
  $payload = $m.Groups[2].Value.Trim()
  $code = ''
  $idea = $payload
  if($payload -match '^`([^`]+)`\s*(.*)$') { $code = $Matches[1]; $idea = $Matches[2].Trim() }
  if($code -match '^(\d{2})·(\d{2})·(\d{2})') {
    $em=[int]$Matches[1]; $eb=[int]$Matches[2]; $ec=[int]$Matches[3]
    $gridId=(($em-1)*250)+(($eb-1)*10)+$ec
    $explicitByGrid[$gridId]=[pscustomobject]@{chatNumber=$chatNumber;text=$idea;code=$code}
    $explicitCount++
  }
}

# 0001–2800: index 10 cells per each parsed B-row of M01–M10.
$matrixText = @{}
$module = 0
foreach($line in $lines) {
  if($line -match '^### M(\d{2})') { $module = [int]$Matches[1]; continue }
  if($module -gt 0 -and $line -match '^\*\*B(\d{2})') {
    $mechanicIndex = [int]$Matches[1]
    $separator = $line.IndexOf('—')
    if($separator -lt 0) { $separator = $line.IndexOf('-') }
    if($separator -lt 0) { continue }
    $cells = $line.Substring($separator + 1).Trim() -split '\s+·\s+'
    for($c=1; $c -le 10; $c++) {
      $id = (($module-1)*250) + (($mechanicIndex-1)*10) + $c
      $text = if($c -le $cells.Count) {$cells[$c-1].Trim()} else {'[REVISAR: celda matricial ausente]'}
      $matrixText[$id] = $text
    }
  }
}

# 0001–10000: deterministic completion of the 40×25×10 matrix described by the chat.
for($m=1; $m -le 40; $m++) {
  for($b=1; $b -le 25; $b++) {
    for($c=1; $c -le 10; $c++) {
      $id = (($m-1)*250) + (($b-1)*10) + $c
      $isExplicit = $explicitByGrid.ContainsKey($id)
      $isParsed = $matrixText.ContainsKey($id)
      $text = if($isExplicit){$explicitByGrid[$id].text}elseif($isParsed){$matrixText[$id]}else{"Aplicar $($mechanics[$b-1].ToLowerInvariant()) sobre $($cores[$c-1]) en $($modules[$m-1]) mediante $($channels[($c-1)%10])."}
      $scope = if($b -in 6,7,10,17,18,22,24,25){'external-or-review'}else{'local-frontend'}
      $source = if($isExplicit){'chat-explicit'}elseif($isParsed){'chat-matrix'}else{'matrix-completion'}
      $status = if($isExplicit -or $isParsed){'candidate'}else{'derived-backlog'}
      $chatNumber = if($isExplicit){$explicitByGrid[$id].chatNumber}else{$null}
      Add-Record @{ id=$id; chatNumber=$chatNumber; source=$source; module=('M{0:00} {1}' -f $m,$modules[$m-1]); mechanic=('B{0:00} {1}' -f $b,$mechanics[$b-1]); core=('C{0:00} {1}' -f $c,$cores[$c-1]); channel=$channels[($c-1)%10]; action='Registrar especificación, estimar dependencia y ejecutar solo tras gate de seguridad'; target=(Get-Target $m); status=$status; text=$text; code=('M{0:00}·B{1:00}·C{2:00}' -f $m,$b,$c); scope=$scope }
    }
  }
}

$ordered = @($records | Sort-Object id)
if($ordered.Count -ne 10000) {
  $sourceCounts = (($records | Group-Object source | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ', ')
  throw "Ledger inválido: $($ordered.Count) registros ($sourceCounts)"
}
for($i=0; $i -lt $ordered.Count; $i++) { if($ordered[$i].id -ne ($i+1)){ $sample=(($ordered | Select-Object -First 12 | ForEach-Object id) -join ','); throw "ID ausente o duplicado en posición $($i+1); sample=$sample" } }
$explicitRecords = @($ordered | Where-Object source -eq 'chat-explicit').Count
$matrixRecords = @($ordered | Where-Object source -eq 'chat-matrix').Count
$derivedRecords = @($ordered | Where-Object source -eq 'matrix-completion').Count

$summary = @(
  '# BELENTANI / JUDAS — LEDGER DE 10.000 IDEAS',
  '',
  "Fuente: $ChatPath",
  "SHA-256 fuente: 0A76776F2714AF733AF7D75A4327AC03AE147E15BB879B58CAE6F26CA9591269",
  "Lectura completa: $($lines.Count) líneas; $explicitCount ideas explícitas indexadas; $matrixRecords celdas matriciales conservadas; $derivedRecords celdas completadas de forma determinista.",
  'Estado: cada idea tiene ID, fuente, módulo, mecánica, núcleo, canal, acción, destino y estado. `matrix-completion` es derivación, no texto literal del chat.',
  '',
  '## Cobertura',
  '',
  "- $explicitRecords celdas con idea explícita del chat: chat-explicit",
  "- $matrixRecords celdas con fila matricial conservada: chat-matrix",
  "- $derivedRecords celdas completadas por matriz: matrix-completion",
  '',
  '## Registro completo',
  '',
  '| ID | Fuente | Módulo | Mecánica | Núcleo | Canal | Acción | Destino | Estado | Idea |',
  '|---:|---|---|---|---|---|---|---|---|---|'
)
foreach($r in $ordered) {
  $safe = ($r.text -replace '\|','\\|')
  $summary += ('| {0:0000} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} |' -f $r.id,$r.source,$r.module,$r.mechanic,$r.core,$r.channel,$r.action,$r.target,$r.status,$safe)
}
$summary | Set-Content -LiteralPath (Join-Path $RepoPath 'BELENTANI_CHAT_10K_LEDGER.md') -Encoding UTF8
$ordered | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $RepoPath 'BELENTANI_CHAT_10K_LEDGER.json') -Encoding UTF8

$manifest = [pscustomobject]@{source=$ChatPath;sourceSha256='0A76776F2714AF733AF7D75A4327AC03AE147E15BB879B58CAE6F26CA9591269';records=10000;explicit=($ordered|Where-Object source -eq 'chat-explicit').Count;matrix=($ordered|Where-Object source -eq 'chat-matrix').Count;derived=($ordered|Where-Object source -eq 'matrix-completion').Count;generatedAt=(Get-Date).ToString('o')}
$manifest | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $RepoPath 'BELENTANI_CHAT_10K_MANIFEST.json') -Encoding UTF8
Write-Output ($manifest | ConvertTo-Json -Compress)
