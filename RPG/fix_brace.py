import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

bad_pattern = r"""            const portal = currentScene\.portals && currentScene\.portals\.find\(p => p\.c === pc && p\.r === pr\);
            if \(portal && !player\.warping\) \{
                    player\.warping = true;
                    loadScene\(portal\.dest, portal\.sc, portal\.sr\);
                    setTimeout\(\(\) => \{ player\.warping = false; \}, 500\);
                \}
            \}"""

good_pattern = r"""            const portal = currentScene.portals && currentScene.portals.find(p => p.c === pc && p.r === pr);
            if (portal && !player.warping) {
                    player.warping = true;
                    loadScene(portal.dest, portal.sc, portal.sr);
                    setTimeout(() => { player.warping = false; }, 500);
            }"""

c = re.sub(bad_pattern, good_pattern, c)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed brace error in update function!")
