import javax.swing.*;
import java.awt.*;

public class westlife extends JPanel {

    private String[] lyrics = {
            "So, I say a little prayer",
            "And hope my dreams will take me there",
            "Where the skies are blue",
            "To see you once again, my love",
            "Overseas, from coast to coast",
            "To find a place I love the most",
            "Where the fields are green",
            "To see you once again........, my love..........."
    };

    private int[] delays = {
            400, 400, 400, 700,
            400, 400, 400, 400
    };

    private int currentIndex = 0;
    private String currentLine = "";
    private int currentCharIndex = 0;
    private ImageIcon backgroundGif;

    public westlife() {
        setPreferredSize(new Dimension(1280, 720));
        backgroundGif = new ImageIcon("sky.jpg");
        
        new Thread(() -> {
            try {
                while (currentIndex < lyrics.length) {
                    if (currentCharIndex < lyrics[currentIndex].length()) {
                        currentLine += lyrics[currentIndex].charAt(currentCharIndex);
                        currentCharIndex++;
                        repaint();
                        Thread.sleep(110); // Delay antar karakter
                    } else {
                        Thread.sleep(delays[currentIndex]); // Delay antar baris
                        currentIndex++;
                        currentLine = "";
                        currentCharIndex = 0;
                        repaint();
                    }
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (backgroundGif != null) {
            g.drawImage(backgroundGif.getImage(), 0, 0, getWidth(), getHeight(), this);
        }
        g.setFont(new Font("Serif", Font.PLAIN, 42));
        g.setColor(Color.WHITE);

        // Hitung posisi tengah untuk lirik
        int stringWidth = g.getFontMetrics().stringWidth(currentLine);
        int x = (getWidth() - stringWidth) / 2;
        int y = getHeight() / 2;

        // Tampilkan lirik di tengah
        g.drawString(currentLine, x, y);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Lyrics Display");
        westlife panel = new westlife();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}
