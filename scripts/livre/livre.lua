-- Filtre pandoc du livre : parties (modules), encadrés, crédits photo.

local function latex(b) return pandoc.RawBlock('latex', b) end

function Header(el)
  if el.level == 1 and el.classes:includes('partie') and FORMAT:match('latex') then
    local titre = pandoc.write(pandoc.Pandoc({pandoc.Plain(el.content)}), 'latex')
    return {
      latex('\\part*{' .. titre .. '}\\addcontentsline{toc}{part}{' .. titre .. '}'),
      latex('\\phantomsection\\label{' .. el.identifier .. '}\\hypertarget{' .. el.identifier .. '}{}'),
    }
  end
end

function Div(el)
  if not FORMAT:match('latex') then return nil end
  if el.classes:includes('encadre') then
    local out = {latex('\\begin{encadre}')}
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, latex('\\end{encadre}'))
    return out
  elseif el.classes:includes('image-seule') then
    local out = {latex('\\begin{center}')}
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, latex('\\end{center}'))
    return out
  elseif el.classes:includes('credit') then
    local out = {latex('\\begin{center}\\footnotesize')}
    for _, b in ipairs(el.content) do table.insert(out, b) end
    table.insert(out, latex('\\end{center}'))
    return out
  end
end

-- Formules repérées par generer.py : <span class="math inline|display" data-tex="…">
function Span(el)
  if el.classes:includes('cjk') and FORMAT:match('latex') then
    return pandoc.RawInline('latex', '{\\policecjk ' .. pandoc.utils.stringify(el.content) .. '}')
  end
  if el.classes:includes('math') and el.attributes['tex'] then
    local genre = el.classes:includes('display') and 'DisplayMath' or 'InlineMath'
    return pandoc.Math(genre, el.attributes['tex'])
  end
end
