import subprocess

java_code = r'''
public class TestBidiFormatter {
    public static void main(String[] args) {
        String[] samples = {
            "የኢትዮጵያ ዋና እና ትልቋ ከተማ ማን ትባላለች?",
            "ታሪካዊው የአድዋ ድል የተከናወነው በየትኛው ዓመተ-ምህረት (እ.ኤ.አ.) ነው?",
            "በ1974 እ.ኤ.አ. በአፋር ክልል ሀዳር የተገኘው እና 3.2 ሚሊዮን ዓመታት ያስቆጠረው ጥንታዊ ቅሪተ-አካል ማን ይባላል?",
            "'AI' የሚለው የቴክኖሎጂ ምህጻረ-ቃል ምንን ያመለክታል?",
            "አንድሮይድ (Android) የሞባይል ኦፕሬቲንግ ሲስተምን የሚያለማው እና የሚያስተዳድረው የቴክኖሎጂ ኩባንያ የትኛው ነው?"
        };

        for (String s : samples) {
            String withLrm = s;
            if (withLrm.endsWith("?")) {
                withLrm = withLrm + "\u200E";
            }
            if (withLrm.startsWith("'") || withLrm.startsWith("\"")) {
                withLrm = "\u200E" + withLrm;
            }

            java.text.Bidi bidi = new java.text.Bidi(withLrm, java.text.Bidi.DIRECTION_RIGHT_TO_LEFT);
            byte[] levels = new byte[bidi.getRunCount()];
            Object[] objects = new Object[bidi.getRunCount()];
            for (int i = 0; i < bidi.getRunCount(); i++) {
                levels[i] = (byte) bidi.getRunLevel(i);
                objects[i] = withLrm.substring(bidi.getRunStart(i), bidi.getRunLimit(i));
            }
            java.text.Bidi.reorderVisually(levels, 0, objects, 0, objects.length);
            StringBuilder sb = new StringBuilder();
            for (Object obj : objects) sb.append(obj);
            System.out.println("Result: " + sb.toString());
        }
    }
}
'''
with open("/tmp/TestBidiFormatter.java", "w") as f:
    f.write(java_code)

res = subprocess.run(["java", "/tmp/TestBidiFormatter.java"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("ERR:", res.stderr)
