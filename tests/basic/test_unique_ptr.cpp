#include "catch2/catch.hpp"

TEST_CASE("test unique ptr", "[unique_ptr]") {
    std::unique_ptr<int> p1(new int(42));
    REQUIRE(*p1 == 42);

    std::unique_ptr<int> p2 = std::move(p1);
    REQUIRE(*p2 == 42);
    REQUIRE(p1 == nullptr);
}