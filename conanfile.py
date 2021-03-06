from conans import ConanFile, CMake, tools
import os

class SOCIConan(ConanFile):
    name = "soci"
    description = "The C++ Database Access Library"
    version = "646efa0"
    license = "BSL"
    depends = "Boost/1.62.0@memsharded/testing"
    url = "https://github.com/SOCI/soci"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "DB2": [True, False],
               "Firebird": [True, False],
               "MySQL": [True, False],
               "ODBC": [True, False],
               "Oracle": [True, False],
               "PostgreSQL": [True, False],
               "SQLite3": [True, False]}
    default_options = "shared=False", \
                      "DB2=False", \
                      "Firebird=False", \
                      "MySQL=False", \
                      "ODBC=False", \
                      "Oracle=False", \
                      "PostgreSQL=False", \
                      "SQLite3=True"
    generators = "cmake"

    def requirements(self):
        if self.options.DB2:
            assert False, "DB2 not supported yet"
        if self.options.Firebird:
            assert False, "Firebird not supported yet"
        if self.options.MySQL:
            assert False, "MySQL not supported yet"
        if self.options.ODBC:
            assert False, "ODBC not supported yet"
        if self.options.Oracle:
            assert False, "Oracle not supported yet"
        if self.options.PostgreSQL:
            assert False, "PostgreSQL not supported yet"
        if self.options.SQLite3:
            self.requires("sqlite3/3.14.1@rdeterre/stable")

    def source(self):
        self.run("git clone https://github.com/SOCI/soci")
        self.run("cd soci && git checkout {}".format(self.version))
        tools.replace_in_file("soci/CMakeLists.txt",
                              "project(SOCI)", """project(SOCI)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()""")

    def build(self):
        cmake = CMake(self.settings)
        flags = []
        flags.append("-DSOCI_SHARED=ON" if self.options.shared else "-DSOCI_SHARED=OFF")
        flags.append("-DSOCI_STATIC=OFF" if self.options.shared else "-DSOCI_STATIC=ON")
        flags.append("-DWITH_DB2=ON" if self.options.DB2 else "-DWITH_DB2=OFF")
        flags.append("-DWITH_FIREBIRD=ON" if self.options.Firebird else "-DWITH_FIREBIRD=OFF")
        flags.append("-DWITH_MYSQL=ON" if self.options.MySQL else "-DWITH_MYSQL=OFF")
        flags.append("-DWITH_ODBC=ON" if self.options.ODBC else "-DWITH_ODBC=OFF")
        flags.append("-DWITH_ORACLE=ON" if self.options.Oracle else "-DWITH_ORACLE=OFF")
        flags.append("-DWITH_POSTGRESQL=ON" if self.options.PostgreSQL else "-DWITH_POSTGRESQL=OFF")
        flags.append("-DWITH_SQLITE3=ON" if self.options.SQLite3 else "-DWITH_SQLITE3=OFF")
        flags.append("-DSOCI_TESTS=OFF")
        self.run('cmake soci %s %s' % (cmake.command_line, " ".join(flags)))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/soci", src="soci/include/soci")
        self.copy("*.h", dst="include/soci", src="include/soci")
        self.copy("soci-empty.h", dst="include/soci", src="soci/include/soci/empty")
        if self.options.DB2:
            self.copy("soci-db2.h", dst="include/soci", src="soci/include/soci/db2")
        if self.options.Firebird:
            self.copy("soci-firebird.h", dst="include/soci", src="soci/include/soci/firebird")
        if self.options.MySQL:
            self.copy("soci-mysql.h", dst="include/soci", src="soci/include/soci/mysql")
        if self.options.ODBC:
            self.copy("soci-odbc.h", dst="include/soci", src="soci/include/soci/odbc")
        if self.options.Oracle:
            self.copy("soci-oracle.h", dst="include/soci", src="soci/include/soci/oracle")
        if self.options.PostgreSQL:
            self.copy("soci-postgresql.h", dst="include/soci", src="soci/include/soci/postgresql")
        if self.options.SQLite3:
            self.copy("soci-sqlite3.h", dst="include/soci", src="soci/include/soci/sqlite3")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs.append("soci_core")
        self.cpp_info.libs.append("soci_empty")
        if self.options.DB2:
            self.cpp_info.libs.append("soci_db2")
        if self.options.Firebird:
            self.cpp_info.libs.append("soci_firebird")
        if self.options.MySQL:
            self.cpp_info.libs.append("soci_mysql")
        if self.options.ODBC:
            self.cpp_info.libs.append("soci_odbc")
        if self.options.Oracle:
            self.cpp_info.libs.append("soci_oracle")
        if self.options.PostgreSQL:
            self.cpp_info.libs.append("soci_postgresql")
        if self.options.SQLite3:
            self.cpp_info.libs.append("soci_sqlite3")
