import org.junit.Test;
import static org.junit.Assert.assertTrue;

public class ExampleTest {

    @Test
    public void testSuccess() {
        assertTrue(true);
    }

    @Test
    public void testFailure() {
        assertTrue(false);
    }

    @Test
    public void testError() {
        Object o = null;
        o.hashCode();
    }

}
