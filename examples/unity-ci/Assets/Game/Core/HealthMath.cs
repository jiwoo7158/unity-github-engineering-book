using System;

namespace AsterArena.Core
{
    // Engine-independent logic: suitable for Edit Mode unit testing.
    public static class HealthMath
    {
        public static int AfterDamage(int current, int damage)
        {
            if (current < 0) throw new ArgumentOutOfRangeException(nameof(current));
            if (damage < 0) throw new ArgumentOutOfRangeException(nameof(damage));
            return Math.Max(0, current - damage);
        }
    }
}
