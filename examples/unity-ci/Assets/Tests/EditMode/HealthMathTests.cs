using System;
using NUnit.Framework;
using AsterArena.Core;

namespace AsterArena.Tests
{
    public class HealthMathTests
    {
        [Test]
        public void DamageNeverProducesNegativeHealth()
        {
            Assert.AreEqual(0, HealthMath.AfterDamage(3, 10));
        }

        [Test]
        public void DamageReducesHealth()
        {
            Assert.AreEqual(6, HealthMath.AfterDamage(10, 4));
        }

        [Test]
        public void NegativeDamageIsRejected()
        {
            Assert.Throws<ArgumentOutOfRangeException>(() => HealthMath.AfterDamage(5, -1));
        }
    }
}
