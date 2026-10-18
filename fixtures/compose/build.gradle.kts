// Compile-only fixture for the skill's Kotlin snippets (scripts/compile_snippets.sh).
plugins {
    id("com.android.library") version "9.1.0"
    id("org.jetbrains.kotlin.plugin.compose") version "2.3.21"
}

val m3 = providers.gradleProperty("m3").getOrElse("1.5.0-beta01")

android {
    namespace = "snippets"
    compileSdk = 37
    defaultConfig { minSdk = 24 }
    buildFeatures { compose = true }
}

kotlin {
    compilerOptions {
        optIn.add("androidx.compose.material3.ExperimentalMaterial3ExpressiveApi")
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.09.00"))
    implementation("androidx.compose.material3:material3:$m3")
    implementation("androidx.compose.material3.adaptive:adaptive:1.3.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.10.0")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.10.0")
}
