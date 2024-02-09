# CHANGELOG



## v2.0.0 (2024-02-08)

### Breaking

* chore(ci): proper commit message

Properly perform a breaking change commit

BREAKING CHANGE:

The first proper breaking commit, due to a misunderstanding of GH desktop; my preferred commit environ ([`96287d8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/96287d8a996b5dcb32abc13dd74570e08bb75324))

### Chore

* chore(ci): Manually update semver

Also drop the semver workflow, seeing as how it doesn&#39;t like branch protection rules. Perhaps in the future it could createa a PR for merging staging into main? ([`2c789c9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2c789c9133cac9b8b135e802042c7df4808198f8))

* chore(ci): Update SemVer Token ([`8183c94`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8183c94a418a9ce0d30269eaf3143ec731c9339b))

### Unknown

* Merge pull request #12 from MAK-Relic-Tool/staging ([`b8a3b16`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b8a3b169002f637bd33ec1f6970a4a85cf134d90))

* Add auto-semver

chore(sem-ver): Add semantic-versioning CI

Relies on Angular-style commit messages to determine if an update is necessary.
The following doc can help: https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits

BREAKING CHANGE: previously, I was hoping to use labels in PRs to specify whether a Major, Minor, or Patch needed to update, and I still *could* do that, but this seems as good as any solution, as long as it works. ([`24cf062`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/24cf0623fe4536730fdec6ea57da2c62b03d1604))

* Fix plugin group command bug (#11)

* PluginGroup default command

- `CliPluginGroup` now has a default command which prints the usage to stderr

- Added `argv` to _run to allow proper name printing if an `UnboundCommandError` is raised on a `CliPluginGroup`
  - `CliPluginGroup` has a `command` name of None for some reason; reading from argv allows us to fix that manually

* Update Test Cases ([`8b6ff7c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8b6ff7ced90775669e9d5c8ae7917b25bafaca7f))

* Features Required for SGA 2.0 + More (#10)

* Create entrytools.py

Finally do that thing where I refactor EntryPoint Registry into Relic-Tool-Core
MAK-Relic-Tool/Issue-Tracker#12

* Lazy load CLI plugins

CLI entrypoints cause a race condition which causes import errors

* Use importlib over pkg_resources

* Begin replacing Magic Word functionality of mak-tools

The only thing that I kinda want from the mak-serialization-tools is the magic word class helper; its nice to not have to import a function to validate

* Magic Word replacement for mak-tools

* Migrate to importlib.metadata

* Formatting

* Formatting and doc-strings

* Trying to update docs

* docs

* Create .pre-commit-config.yaml

* Run Pre-Commit

* Move to pyproject.toml

* Add Mypy to precommit

* Update .pre-commit-config.yaml

* Update mypy.yml

* Update .pre-commit-config.yaml

* EntryPoint fix for Py 3.9

* Fix requirements

Not proper utf-8 files

* Pylint / MyPy Fixes

* Mypy Cli fix

* Update pyproject.toml ([`45c27e3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/45c27e3bd97516c37be88e96521037cde2a585d2))

* Better CLI explanations (#9)

- `relic_cli` is now `CLI`
- `CLI` is not exposed directly by the `core` package
  - allows `from relic.core import CLI` which just looks nicer
- Updated Readme for Usage guidelines
  - The core library doesn&#39;t offer much utility outside of the Command Line, the readme reflects that ([`62bf12b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/62bf12bbf7c1c90a07c84cb9bb4d88541b3dcc17))

* Fix CI integration failures when setting up Staging branch (#8)

* Buffer not defined because typing-extension not installed

* Fix name no longer supporting None

* Resolved TODOs

* Update .pylintrc to properly calculate score, also lower pylint standards

* Docstrings + Formatting

* More docstrings + raising proper Errors

* More docstrings and lowering pylint standards

* Apply Black ([`a3ff7f7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a3ff7f757e8d2a208610fc9a8e168bd281147ba1))

* Merge pull request #7 from MAK-Relic-Tool/main

Update workflows (#6) ([`8722c6c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8722c6ce25f33a697908c8a38cedaf05d736bab8))

* Merge pull request #5 from MAK-Relic-Tool/SGA-2.0-Alpha

Updates to Relic CLI `run_with` and new `lazyio` module ([`922dad0`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/922dad005b0bc09a5663274c048df38d17c22ea0))

* Update workflows (#6)

* Update pytest.yml

* Update pylint.yml

* Update black.yml

* Update mypy.yml ([`fe3fbf2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fe3fbf2a930a6dd70ce718c3a927ab5aabfd88eb))

* MyPy | Black | Pylint fixes ([`b8f795e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b8f795e269569ae29c0c3a13b9c31cb2822ea69d))

* Fix pylint score function ([`433a481`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/433a481b947e4f6a97f47aa93be8ac60661a0559))

* Refactored from sga.core + new interface for lazy reading/writing

The old method exposed a lot of extra properties on classes which didn&#39;t need to expose that; since their job was to read/write sections of the stream.

The new method uses composition instead of inheritance; but allows for inheritance chains to continue to work by using the BinaryProxy protocol.

This primarily allows the &#39;serializers&#39; to continue to act as BinaryIO objects without exposing all the BinaryIO info ([`25dee09`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/25dee098f2857253523f747a0e60d6178a9607b6))

* Black ([`fc07651`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fc07651c9d6640cb38e2f3213f67db6dd9bc71af))

* Allow run with to ignore &#39;program name&#39; when passed ([`aaaffba`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/aaaffba1f6563773a39c35e0c4fd1ea0045ae2e9))

* Test Cases &amp; Bug Fixes ([`fe87852`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fe87852bfcf962320f657601e646af83476bb93a))

* Lazy IO

Makes reading faster by not doing it ([`ef2587c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ef2587c523dbcad2895c1687d82157f60e85d401))


## v1.1.1 (2023-10-15)

### Unknown

* Merge pull request #4 from MAK-Relic-Tool/add-cli-support

Hotfix for `run_with` &amp; `_load` ([`76895fd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/76895fd4b0d5366b7ce61132d5c2db8f20d9ce52))

* MyPy Fixes ([`b2daa72`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b2daa7224a018126e2f8cb01c514d7626de83be9))

* Fix tests failing due to argparse difference per version

3.9 uses `optional arguments:`
3.10+ uses `options:`

This means we can&#39;t do explicit comparisons (without checking the version)
So we compromise by checking an expected value in the output. ([`88c7a9f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/88c7a9f429d646c0feb3457e9db148f7400e8c32))

* Bump to V1.1.1 (hotfix) ([`7bae819`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7bae8195b0546573f3605811a6dc295c37a5bffb))

* Run With Fix using sys.exit

Run With, being a &#39;library&#39; version of the cli, shouldn&#39;t perform a sys.exit, as that would then clsoe the calling application ([`f772bdc`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f772bdc7f17d9b23a3f55af0e4bee89dbf6aa8af))

* Merge pull request #3 from MAK-Relic-Tool/add-cli-support

Add cli support via a `relic` entrypoint group

Any function accepting a `parent` SubParsers object can be used as an entrypoint, but `CliPluginGroup` and `CliPlugin` are provided to quickly create command groups and groups. ([`4107caf`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4107caf3b3882da288b3c356fd3725340b49022d))

* Remove autoload parameter

Remove autoload parameter; lazy-loading in a CLI/plugin system can cause confusion when something that is expected to be there is not because it was not requested. ([`615d187`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/615d18740f884062c17e35b699f21853b2960cec))

* Create test to check CLI installed

Local testing requires the package be installed locally, which can make things weird when testing locally ([`346ebed`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/346ebedb788ab21fa77b7a0fe376ad62b53a2898))

* CLI runner created and console_script hook added ([`c507eeb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c507eebd4a7966fc42090954dc1bd1c4e03f7a23))

* CliPlugin &amp; CliPluginGroup now have paramater-less inits ([`b094e11`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b094e114545599838269c321a76409e69fef040f))

* Run / Run_With to distinguish CLI / Lib use

Both perform the same function, but run grabs from sys.argv, and run_with grabs from the provided arguments ([`1460edf`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1460edfb531735dfc48b830609fe6128255e418f))

* MyPy | Black | Pylint fixes ([`cdc093e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/cdc093eeca674101cbe5c87efc8f0148cd692317))

* Update .pylintrc

Lower the bar a bit, and fail on errors ([`d6d4000`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d6d400059bc1d487d1bccf63f2fb032769815ffc))

* Create black.yml ([`7852a19`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7852a190a8d97f05add029fc3a5fe54fc8542d46))

* Bump version ([`ebe88a2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ebe88a24ec164b25d4f2e1390ed3d7b680427b7d))

* Create cli.py ([`b44ac48`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b44ac4824951aa1bc8a575cfcd035d96299b1ab9))

* Update metadata ([`4c0b2db`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4c0b2dbbd15cebe2566fd33c1392e2a206b84de7))

* Merge pull request #2 from MAK-Relic-Tool/fix-#10

Explicit None Checks in `_print_mismatch` ([`90e444d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/90e444d94213d0f53583cfcf101465bae4e0834f))

* Bump to 1.0.4 ([`80b0d60`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/80b0d60eab029e57c55cc471a16afb5ef6f14c76))

* Explicit None checks for `_print_mismtatch`

Should prevent falsy values from not being displayed properly. ([`08996d7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/08996d76e65f272bef924923a965eed7f2ca67da))


## v1.0.3 (2022-09-27)

### Unknown

* Merge pull request #1 from MAK-Relic-Tool/mypy-fix

Enabled mypy support when installed as a dependency. ([`05caac5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/05caac5f3c7b6cd94e7a35906a08076dfa659022))

* Enable mypy support

This fixes two issues preventing mypy from recognizing this package&#39;s inline types:
1) py.typed was not in the package level directory
2) py.typed was not included in the MANIFEST.in ([`78c0377`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/78c03777d7a92995a4b29b9bbabc3804afb70dcd))


## v1.0.2 (2022-09-27)

### Unknown

* Readme fix badge, bump to 1.0.2

Another cosmetic-only fix ([`6090fb8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/6090fb8a0a12f06d5faf8cae21e1c4584a4d6645))


## v1.0.1 (2022-09-27)

### Unknown

* Bump to v1.0.1 + setup.cfg metadata fix ([`bbf7e26`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bbf7e261ade58afb75d56a0fee157fd0f4202141))

* Update publish-pypi.yml

Add workflow dispatch to manually publish failed runs ([`9340ca8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9340ca864b911a251af65355dbd563c50e453afc))

* Update publish-pypi.yml

Potential fix to publish-pypi

The joy of workflows is that you have to run them to debug them ([`e33f16c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e33f16c19472ffd90d14f33965127b907d706bce))


## v1.0.0 (2022-09-27)

### Unknown

* Update errors.py

Pylint whined about the &#34;...&#34; ([`b53ed01`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b53ed01a74f78b75acb5b03d741a55ffc276c7e2))

* Adds RelicToolError &amp; associated regression tests ([`31f28a6`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/31f28a67290bc32c93f4e8f98aaebaecad2377e3))

* Update README.md ([`21d2b37`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/21d2b376d206af1f5e890a63b6d874e711c15b0f))

* Update .gitignore ([`510904b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/510904b4c19dc7344644aa6acb5fc799a5a97704))

* Use reusable workflows ([`0d0c53d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/0d0c53d823c6a0d40b29b8b3f5a1c1223f23a8e1))

* Update typeshed.py

Fix mypy/pylint errors

__version_pair will break mypy&#39;s version checking ([`c36db75`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c36db75dbc783bb8f58219c3f87617fc98546354))

* Pylint fixes ([`87a6da8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/87a6da8ae176b257b8ee34f0cf0fb80c1ae27082))

* Setup fixes

Version moved from date-based to semantic
Only testpypi has seperate version; while bad; we can delete the old modules (probably) to allow the semantic versioning to pass ([`fa96388`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fa963881c4a30f147a0547621b82d6323dcd0ef3))

* Update errors.py

Explicit __all__ ([`b922f4b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b922f4bc1d5baa69a84d8a8d6463d40087dde936))

* Better Regression Tests

test_errors was mostly just a way to ensure that errors was still included and didn&#39;t really test anything

test_regressions only ensures that the attributes that are expected are exposed ([`68f54f4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/68f54f4c4c6ab27afe6e4e427d5938e51a234dd8))

* Black + Typeshed implementation

Somewhere in the refactoring I lost typeshed.py ([`65ded94`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/65ded947dfd7537af0a5b27a7e795ee7ec169da9))

* Update Readme/Fix Manifest ([`8825cfe`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8825cfeba3d34601a47aa2eeb81bb36fe2b461ba))

* Update setup.cfg ([`665d337`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/665d3373d0028565e2010f2294ac27ab9ee3090a))

* Merge branch &#39;Drop-Non-Core-files&#39; of https://github.com/ModernMAK/Relic-Tool-Core into Drop-Non-Core-files ([`1f1830f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1f1830f0f945b9ed27c9c8f1d39a3aa2f4a676f1))

* Merge branch &#39;Drop-Non-Core-files&#39; of https://github.com/ModernMAK/Relic-Tool-Core into Drop-Non-Core-files ([`073cf76`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/073cf76660966686e87cbe0c62c380d14ab0e62f))

* Update README.md ([`7e6680c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7e6680c436ed96341be330028eaffbf454d8b79b))

* Merge branch &#39;Drop-Non-Core-files&#39; of https://github.com/ModernMAK/Relic-Tool-Core into Drop-Non-Core-files ([`9bc96a0`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9bc96a089c0ec658469adb66652eb45a28de1753))

* Black Formatting ([`ca93d13`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ca93d138e0abf70f69da894951f97f4f13a8fe85))

* Prepping for SubPackage ([`b909053`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b9090539e8ad8715f3f049c44ca1ae08bfbcd349))

* Prepping for SubPackage ([`9a17046`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9a17046c515cf530497f1c50d893178942ca1fa3))

* Droping files not in Relic.Core package

For my sanity; I&#39;m finally doing it

For the most part; SGA/Chunky/UCS don&#39;t depend on each other

Yes; SGA can use Chunky to extract a chunky&#39;s contents in place; but then you could just use both packages separately.

Likewise; UCS is helpful when writing better names for SGA extraction; but then both packages can be used in the same script.

Core doesn&#39;t have any features itself; it&#39;s merely shared code between packages; like Errors ([`6554d13`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/6554d1326533bafc5415cc11a8027f485cc43bed))

* More MyPy/Pylint/Sphinx updtates for SGA ([`ee37477`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ee37477e6188148ebc91ab88f2e7d1b39a0ae1bf))

* docs + mypy ([`84f95af`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/84f95af2e36af05d4bd0373e42ffd6943a07f157))

* relic/sga mypy support

should be perfect; but after linting I&#39;ll probably break it somehow ([`632b9fd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/632b9fd4c69782352b2301cbd0b8bd60eddedb01))

* Update workflows/readme from Main ([`e8ba5cd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e8ba5cd42c410754b38200a789e779170b4f9a1f))

* Update .pylintrc ([`673057b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/673057b842f3780a2f1b9a6acc3eb847b5ad3bcc))

* Update README.md

Add badges for pylint/mypy (non-workflow badges) ([`7b1c812`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7b1c812cbc5f154041c7ca341392d2b34e163b4f))

* workflows run when settings change ([`1c484e1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1c484e194d5dffe4644cc887b67f2b1474f2f2e9))

* Update MyPy / Setup Pylint ([`c3fb2b9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c3fb2b917f268dbd43fb82ae80f665004260a455))

* Linting / Type-Checking / Docs ([`d5b71ed`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d5b71eddd5cf762adc2939962fae139e890f97fd))

* Potential fix for scripts

Scripts need their own test suite too; and boy that&#39;s gonna suck ([`bd51f96`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bd51f96b3b3b470cdd288224eee8e9645b05792d))

* relic normal package instead of namespace package

I severely misunderstood how namespace packages are meant to be used.

I wanted to split the app into separate subpackages to allow &#39;granular&#39; installs; primarily for the eventual update of the blender plugin

But that would require writing individual setup.cfg and setting up CI to handle that is just plain bad without splitting each subpackage to a seperate repo (unless you can tag branches?) But then changes to other subpackages gets screwy.

Rather than deal with that hassle; just making it a normal package and not dividing everything up seems like a good idea now ([`eda57ec`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/eda57ec66a23d0561b6cc4be5dc3dc422db55115))

* Update .gitignore ([`0a892bf`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/0a892bf1d7c0dfc98a14d54f6d59c22ad6b43237))

* chunk_id =&gt; ChunkCC ([`ebeec32`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ebeec3276262bfef72e1d9bb13f3f17676a26b87))

* Merge branch &#39;refactor-chunky&#39; into refactoring ([`b572bb9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b572bb95734d822704d78cb1c1ced8a2264dede9))

* new api for chunky

It doesn&#39;t feel as good as SGA

Chunky wants more flexibility than SGA

SGA is self-contained; all that functionality can safely be implementation dependent; Chunky wants to define subchunks explicitly for modding (whereas sga&#39;s very simple, folders/files) ([`17c456c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/17c456c9069d259c0ec1dd04cde16d94f59c7423))

* Merge branch &#39;refactoring-sga&#39; into refactoring ([`3378591`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3378591910fa5d03ca09ce1d7a4c0c563ffa9dcf))

* Update .gitignore ([`e83e59e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e83e59ed6f2b860f6b4fae5bbbe833dd0df98ffd))

* inprog commit ([`24428eb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/24428ebf142c06bab6bf0bbfcb2292fa0c6e19e4))

* Update setup.cfg

Fix setup.cfg not using find_namespace for new &#39;relic&#39; namespace package ([`27eb8c3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/27eb8c3deae1ee6e180f1d7ba3add75ee6c56663))

* Update mypy.yml ([`d6a6340`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d6a634098947fc1755c95f852818852d2dfe5d88))

* Update README.md

Add MyPy badge ([`1f5c074`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1f5c07423e84a2aa759cc6999b65e0186240eda0))

* Revert &#34;Update mypy.yml&#34;

This reverts commit 1817ea9f575b29c23a74d57e83b353412a43581e. ([`92d271f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/92d271f96dc1ac47ecbe0d1387f01486e1f0a9ee))

* Revert &#34;Update mypy.yml&#34;

This reverts commit 12879728ce403dd198f652ba567a11c845095818. ([`887cb5b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/887cb5bd613e9503355d5f40c979ffb62e42beb9))

* More MYPY fixes ([`f0a9256`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f0a9256729761b587bcb19f11a4131db1ff9dd03))

* Update mypy.yml ([`1287972`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/12879728ce403dd198f652ba567a11c845095818))

* Update mypy.yml

I think I understand how `-p` works; it doesn&#39;t expect a package; it treats the path AS a package. Or something like that, hopefully this is the last CI for mypy ([`1817ea9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1817ea9f575b29c23a74d57e83b353412a43581e))

* Update mypy.yml

I caved; mypy now just uses the src/relic directory instead of building the package ([`db3de99`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/db3de99ce5aae3e1622e4a661b3b1f0f6aa4e190))

* Update mypy.yml

Maybe it want&#39;s the pypi name instead of the package root name? ([`284acc4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/284acc415d96f0ddea6231218a30ce1ca4eae33c))

* Update mypy.yml ([`fe36242`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fe36242b3d6fd27520e6dd25aa06fc0b37bde87e))

* Update pytest.yml

Hopefully this will stop running pytest on non package changes ([`9e8eeea`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9e8eeead25c3acbbd639fadb1e561970b197abac))

* Update mypy.yml ([`e954474`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e954474e4257b376959e581ae81fe66ba2a4c0d1))

* Update mypy.yml

the action im using will run mypy on &#39;.&#39; if i don&#39;t specify path; since im building the module and then running mypy -p package, hoping this will  only do checking on the package and not on src files ([`7c4bbd4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7c4bbd4b775bfb168ef47cf1f887f09715aab4cd))

* Create mypy.ini

For mypy action ([`2d5a3d8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2d5a3d87c7c4794b57f5c2ba768249967d17e3b6))

* Add MyPY action

First steps to supporting a fully typed-package; implement type checking CI ([`c926bc7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c926bc7af783f37fdf607740502de94f8dd86d56))

* more refactoring / setting up testing ([`85a8f67`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/85a8f67259ff846b92be64795960e747b2876fba))

* Make relic a namespace package ([`f560f79`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f560f79849c16f226abaea967fa1cb3413d7c3ee))

* Mypy refactoring ([`32451b3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/32451b3c48161f95fdb9999423f4b5ee2640119b))

* Update .gitignore ([`73a586e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/73a586ef4a75b6cca879adef681213977518abcb))

* Cleanup old test

Most of them are going to be rewritten completely; ([`1ff11fe`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1ff11fe9b9b1d96579e6c9dc55a06080c5cab687))

* rename error.py to errors.py ([`186a1eb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/186a1eb6eb688999c2f23931f4590bc204924b83))

* New API, No CI Tests

A lot of code is &#39;rewritten&#39; instead of shared between versions; but I consider this a &#39;feature&#39; for the most part.

I&#39;m sure I could hack something together, but this looks much cleaner then my previous two rewrites.

Unfortunately, unlike the previous rewrites, tests were extremely broken; as &#39;headers&#39; are replaced by metadata or ignored (due to being redundant).

Rather than fix them in this commit; I added the ability to test against file sources on the local machine; in other words, I can test against REAL data. Unfortunately, unless I build my own dataset, this won&#39;t be used in CI to avoid distributing relic&#39;s assets. ([`b180cf0`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b180cf021476f0b67edb4d8f55db8a6151398167))

* Update .gitignore ([`bb0a6b6`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bb0a6b62fdf23f74e4f36f82d5b46abb2c2c9680))

* progress commit ([`88f665a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/88f665a9738eeb13c3ef00cfcd9159d6143707ae))

* Drop old sga ([`2ca3467`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2ca3467c4f1fa757a2a5cd453c586102e3f24471))

* New API for SGA (v2/v5/v7/v9)

It still really sucks; but to avoid the problem that the OFFICIAL RELIC ARCHIVE TOOL has; each `version` reimplements it&#39;s own codebase

I get around this as much as I can with ABCs but it is ugly.

Ranting about official Archive Viewer; admittedly, they are distributed with CoH2 (and DowIII) so as long as it works for those formats; great! But then why bother supporting past formats?

Dow II (v5) is among the formats which is supported (v4 is the earliest supported according to their version-assertion logic; COH1 I assume) but the checks to support that format don&#39;t seem to line up with my own research

I&#39;d have assumed this was because the switch to the Essence Engine (over whatever DOW1 uses) but COH2 and DOW2  both use the new Essence engine; so... ?

As an aside; that explains why DOW1&#39;s enumerations for FileStorageType are different.

I pray this is the last time I rewrite this API; I moved away from the clunky &#39;make no assumptions&#39; strategy I had done before (which was very straightforward, but a lot of boilerplate) with a simple read/write at the archive level; with unpack/pack for helpers used for serializing data .

I need to get better at typing (figuring out generics of some kind) to make ArchiveABC  auto-type things like Folder/File/Drive definitions and their respective pack-aware helpers.

We also stop using those nifty ptr objects; as much as I liked the idea of &#39;slicing&#39; a binary stream; it&#39;s annoying to debug, and only hides where a stream is pointing:

perhaps using a slice which only warns/errors when reading/writing outside the bounds (allowing seeks); and will only read to the &#39;end of the slice&#39; ([`5b545a6`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5b545a68c0d6c76fdc1e9d2a43821abaa181bef0))

* Rewriting now that I have a better understanding of the binary layout

Before I was rewriting to keep versioned code together; which ill still do; but now that I see that the SGA follows a pretty straightforward layout (for v2-v9)

I think I can refactor a lot of excess code out ([`6f440f1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/6f440f14d4aba5e24ccfcb7c143fdeb51aeb5f84))

* v7 support? ([`91f93a3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/91f93a342e08976745bffb6df594381168d3bd60))

* Fix v9 tests ([`934fdf7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/934fdf721d8f83e336464f110a7f0ec5acb609a4))

* SGA script fix ([`8204f88`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8204f88f2f45bff06a245fd23a42014ffd03e194))

* pytests refactored to match version-refactoring

tests pass but the other archive tests should be PRd first; then cherry-picked merged into this one, and fixed for the new API ([`945831f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/945831f984f696a35f910d36dfd5590eb089b152))

* Refactoring SGA

To reduce the tight coupling of &#39;Versioned&#39; classes and their Unversioned base; the unversioned base no longer contains any version lookups.

Instead; the APIvX protocol should be used to get/specify types that each version is expected to have

This refactoring breaks alot of the old codebase; which expected most versioned types to &#39;figure it out&#39; by being passed the version and the stream

The new APIvX format should ensure that
A) modules that want to be vX compatible define their &#39;version&#39; of the vX classes (vX defines a helper to determine if a module has been properly defined as an API)
A.1) While modules can be apis, the preferred method is to use APIvX objects; while following the vX module syntax format for imports
B) &#39;Simple&#39; to define their own arbitrary vX formats: Simply create a class with classvars and set the classes to their appropriate hook.
C) Registering versions is done in a single location; before each individual class needed to update a lookup table with the versioned classes &amp; there was only one global table (per class), meaning swapping the version contexts was impossible. Now, we still have one global lookup table; but it&#39;s easier to pass a version lookup table and avoid worrying about ensuring other tables are up to date

This is kinda a rant, but this is a massive API change
With tests not fully implemented for SGA, alot of functionality is broken; and the tests created need to be refactored to account for the changes ([`00a5727`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/00a57277fd296ad421a9104806ce18549b48104c))

* Merge pull request #17 from ModernMAK/Implementing-Tests

Implement SGA FileHeader Tests ([`45c4e5d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/45c4e5d152c3982fd10c6dda12df5041802045f8))

* FileHeader tests ([`d770eb3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d770eb34d96531927437cfef504e3822070983ea))

* Organized datagen / simple file_header tests ([`51f14fa`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/51f14fac5c841f6d80daa85284529470446a968e))

* Better Datagen for testing DowI sgas

Should cover most required test cases; and is still independent from the packing logic ([`335c7fd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/335c7fdbf4f5459688163f3492c9d1b61f285e88))

* Merge pull request #14 from ModernMAK/13-implement-relicsgaarchivearchivepy-tests

Tests for `relic.sga.archive.py` ([`53c805f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/53c805ff1d3b6a6635bf67ac5022f7afc25c610a))

* Tests for relic.sga.archive

pack() currently allows NotImplementedError, but will expect the archive to match a precalculated buffer

This should be refactored to __eq__ the unpacked archive; as archive&#39;s do not need to repack the data in the exact same layout (Especially since V5/V9 specify TOC ptrs) ([`16c315f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/16c315f1e68b7fb65fc6ce479cc880ee2f6008ed))

* Merge pull request #12 from ModernMAK/6-add-tests-for-relicsga-module

Add Tests for `relic.sga.archive.header.py` ([`6656d0c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/6656d0c8bc0c99b8160061cf9584693de896f033))

* Fix Readme / Add Links to Badges ([`dee0a52`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dee0a52c95412229fa5caa6f521404557656a7dd))

* Implemented Checksum validation tests

Begrudgingly added archive tests

Will cry when I break them later

Mostly just wanted that pretty green checkmark and to close #12 for good ([`985401c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/985401c43e57547842a8abab7d2eb7b78a7f6001))

* Fix Imports ([`bac9f54`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bac9f544c75effaca7d15a8e1ff7765fb60b7179))

* Merge branch &#39;bugfixes-found-while-testing&#39; into 6-add-tests-for-relicsga-module ([`fbb0fa1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fbb0fa170ba9c4850b999ad9a88f976f52bd993c))

* Tests for DOW I / III ([`937d8cd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/937d8cdcbe64779150a3ad66a925b6a1c74e2cac))

* Fix DOW I / DOW III Archive pack/unpack ([`46fceb8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/46fceb829cfc7a9c88b6e8fb4f7ad9af42dd35fc))

* Merge branch &#39;bugfixes-found-while-testing&#39; into 6-add-tests-for-relicsga-module ([`8d7b026`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8d7b026932b9561a7af546b7c9c78afd5331f0ac))

* Don&#39;t convert csums to string ([`b9930b9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b9930b92546275d0d70b7a6a4f3e309b08bab5fa))

* Tests for Dow2 Header ([`86200cc`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/86200cc238542dafef8f6282b29b50ae5bfe5916))

* Merge branch &#39;bugfixes-found-while-testing&#39; into 6-add-tests-for-relicsga-module ([`f560e43`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f560e4373d7430a6fe38f67b57fb2800ff2d5d32))

* Fix name not being encoded before packing ([`2d13060`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2d1306097f421b4da2f143d53185ad04209464ec))

* Merge branch &#39;bugfixes-found-while-testing&#39; into 6-add-tests-for-relicsga-module ([`47da990`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/47da9905740b91e152763a7c5c669762013831f0))

* More tests for header ([`de8ed3d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/de8ed3da22f9b6410e9deaeaee52b82e4b653fa0))

* Fix name not being encoded before packing ([`b346859`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b346859d2e1f62e2acdcf1b52d0540e8d7ee9909))

* Dow3 Header using ArchiveVersion Dow2

Most likely a bug, will need to test against Dow3 dumps ([`f7e09bb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f7e09bb772d808a9aef8ee5b0af65f2427439689))

* Update test_header.py

Added some actual tests ([`41f43ba`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/41f43bab8f4bd7b76dc7d2ce2bbd33f4314119ae))

* Create publish-pypi.yml ([`3e14fef`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3e14fef4a01aa95ae682b523badf5bed4f9a6917))

* Merge pull request #3 from ModernMAK/rename-archive2serialization-tools

Fix Tests Not Passing
Dropped Py3.7 / Py3.8 support; serialization_tools doesn&#39;t support less than Py 3.9
Renamed archive_tools to serialization_tools to account for module renaming
fixed relative import for tests
 Updated pytest CI to build package and test against that instead of testing against code
Version primed for 2022.0-rc0 ([`eb285be`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/eb285be28b70652dc63489545369d1c0c3839d8c))

* Update pytest.yml ([`4f666ce`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4f666cee37dfb31dc772587fc702a8e317445498))

* PyTest against package instead of code ([`73ff923`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/73ff9234dcea82704a5eec07ab628f216b0bff93))

* Merge branch &#39;rename-archive2serialization-tools&#39; of https://github.com/ModernMAK/Relic-Game-Tool into rename-archive2serialization-tools ([`b821df5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b821df5f23505afa98cc28fb7b327af662878a75))

* Use absolute import for `tests.helpers` ([`ee75122`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ee75122575c96d94abe1e98f10fa03460336c721))

* Merge branch &#39;main&#39; into rename-archive2serialization-tools ([`19c769f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/19c769ff5a9b92934d7011685d4c516b1e4b39e2))

* Mak Serialization Tools doesn&#39;t support &lt; Py 3.9

No longer test against 3.7 / 3.8 ([`2cb2a6e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2cb2a6e9ff2ea179f4f87c260f62fbc18efa3c89))

* Include Py 3.10 in tests ([`6859582`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/685958295345682852bde23498935338defc12ee))

* Restrict Requirements / Update Version ([`7897841`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7897841a84baf1600b7471c0b7f0a85e0c0fa787))

* archive_tools -&gt; serializaiton_tools

I&#39;m a genius;

create archive_tools.py @ src level
refactor/rename archive_tools.py =&gt; serialization_tools.py
delete serializaiton_tools.py

boom, all package imports are renamed :D ([`9caad89`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9caad89c6b319d72051b61b5ad9658cdb50283ba))

* Merge branch &#39;indev&#39; ([`f65a07d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f65a07d6ad744b5ca5407b36fedf64f19502ead8))

* Update  readme and setup config ([`3b9c734`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3b9c734e9f61295615d8b07f40c503ef2117c1f7))

* Increase version, change req, update name ([`54cf28a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/54cf28ab76c116bd9724c9a093d560e7db52e139))

* Create README.md ([`627579f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/627579f0ad838825c3da3cc02573a99e19a91d73))

* Include enc.exe/dec.exe ([`6996616`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/69966165ad935abb61c4d65a898ceb966d86dbab))

* Formatting, added missing __init__.py, ([`f27b8f7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f27b8f760fecb1486bb8910b255966072fab460c))

* Create LICENSE.txt ([`0284fa1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/0284fa1c5e82d151d38ea6baa71a1755fa5b756e))

* Reorg WHM and meshdata.json support for animations

With no tests we aren&#39;t stable yet, but the rewrite is more or less done

WH3, I haven&#39;t fixed yet, mostly because I didn&#39;t want to install it and dump it&#39;s sgas until I felt done with Dow I and Dow II. ([`033fa80`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/033fa80d710ef11f01062b4c323c355250113c02))

* Animation support maybe, also trailing data is 3 buffers

Probably a secondary pos buffer (12/4=3), but idk on the other two  (24/4=6), (40/4=10)
Maybe Uvs?
Float4, Float2 and Float4, Float4, Float2?
Float3, Float3, could also work for 2nd buffer
Obviously alot of ways to unpack the 3rd buffer; worry about that later ([`00bd6fd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/00bd6fd8acb1563a27429a289e9d2faf8ef82d95))

* Update model.py

Dropped comments; while useful when I was prototyping, it&#39;s making the file a chore to skim through ([`67cf3c9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/67cf3c92ff0ae685d127849a79037408c029ccbf))

* Dow 2 Model ([`9b2debb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9b2debb54beb4d0176751c05b99ecfcf5b20802b))

* Update wavefront_obj.py

Fix normal/uv swapped ([`47aff64`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/47aff642c86f29ce33ab804a5d47e1e9f389c2e2))

* general obj fixed ([`e6223a2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e6223a2d0b9c2a0f1a8c0a93f3b12ec71d2810d3))

* Massive overhaul for model ([`d44a6d2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d44a6d2a0206f1e55618ac894cee313b47f11202))

* Model and refactoring ([`5c464b4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5c464b44d7faf35367280536eac79696c439b3b0))

* Update importer_blender30.py ([`22a8489`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/22a8489c7fff93a9a25139ff86cb94d76ea60397))

* Rename SelfIdentifying to ChunkDescription &amp; some minor WHM notes ([`8c32783`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8c3278364fd2656b3a01e2b988dd5fa31e4f78c2))

* Update importer_blender30.py ([`a82a0eb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a82a0eb3678a4479b97d2ac55ee1ef7ced9896fe))

* UVs, Materials, proper rotation &amp; placement for verts

Bones still look wonky at times, and not all bones are used everywhere

Marauder seems to lack any bones ([`7fbcb68`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7fbcb68f541abb785a8ffb6a35f57817c6b36d5b))

* More Importer features ([`b6fc68f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b6fc68f4a90ccaf0c4ba6fd7b20e8fea4a9e04b6))

* sga unpack / blender importer ([`914fbf3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/914fbf30c73db62a28f5e8d0acd07d3505e028e5))

* Prettify bone creation ([`dc936ad`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dc936ad52ab0c91733918530c7018128f8fa26d5))

* Extractors ([`798ae65`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/798ae65370bb22ac05fdce874beb75ae1c48e9dd))

* Removed redundant scripts

Scripts which now reside in the universal script are removed to avoid duping

The matching script file in the universal hierarchy SHOULD implement the same behavior if running as main. ([`9a2c3af`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9a2c3afd3225cb41de4cc89fceb212d65c553417))

* universal script

While a long master script doesn&#39;t sound too good; flooding the namespace with dump, extract, and others doesn&#39;t sound too good either ([`3968556`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3968556176079b27efa8d052a6e1c084cb76a2f6))

* Working Blender script

working-ish...

Bones work perfectly;
but I haven&#39;t figure out how to convert them properly to blender-space

So the bones can deform the mesh properly, but the bones aren&#39;t in the proper locations

Also some meshes lack boneweights but have skeletons? May be stored in excess? But bones is empty in mesh header? ([`327409a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/327409a6cdb7d8e0afdc389b67c609a9abd6e018))

* blender script works for verts, no bones yet ([`98e8bfa`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/98e8bfab7637e99cfe2aa90c6756bc66b5c0cc7e))

* Found Bone Weights!

I didn&#39;t understand that 16 byte section for some meshes, since it looked like floats, but the 4th &#39;float&#39; was garbage

While debugging missing meshes in my mesh_json script, I accidentally noticed the 4&#39;th float had 0x4/0x5 which matched the ids referenced in the header names. On top of that; those ids and names match names in the skel chunk.

BOOM

Mystery solved ([`8ad195f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8ad195fe2d48574b7fc58664300e1d0d5488b423))

* Scripts for whm2obj, rtx/wtp/rsh 2img ([`ebd17f4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ebd17f4082226e0dee0be5a716f59384c4757d27))

* Fixed width/height swap bug

ATTR was swapping width and height; which wasn&#39;t noticeable for most pow2 textures.

Because order is important, we unpack in the proper order inside convert and use kwargs to set the data class fields. This will allow the dataclass fields to be reordered without accidentally altering data. ([`b0370f8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b0370f830fccf112d40cad8bf3c0e392e5059785))

* Pos,Norm,Uv buffers cracked on WHM?

I&#39;ve had this before, but if I recall correctly, it failed on select files.
While I haven&#39;t validated anything by dumping to obj and importing into Blender, not crashing is a pretty good first step.

Also version went back to year.patch-staging, because it&#39;s really dumb for me to have year.month.date.patch-staging

Fixed TxtrChunk not copying header, and made it SelfIdentifying
Fixed audio_converter not correctly pointing to the converter exes

Convertable now uses List instead of Iterable, and added support for sub_factories (although it shouldn&#39;t ever be needed, since most convert functions don&#39;t know about the converter) ([`dbded11`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dbded1163290cc783397ba16e11aabb63baf6290))

* Packagable ([`f809c8f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f809c8f7bb1b8794fa6acc8b12c5e6f20f0e9377))

* Simple implimentation for all DowI chunkies &amp; archives + FDA dump script ([`2ac9803`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2ac980372cc0bc0a4374b71e17ba9b86cbd570b6))

* Formatting and dropping commented code/repeated files ([`802eae8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/802eae88e999fa549de1164c8dddd9ab32b48e76))

* Added RTX, broke WHM

Some wtp and rtx files are 100% broke; not sure if it&#39;s my fault or not...

Should probably try running my unpacker against another unpacking tool and see if we get differing results ([`36cd1b4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/36cd1b4a2937bf85fb7eb4c8674831744f456ae3))

* More WHM support ([`c4734b2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c4734b277a790a108c03870ab0529c00f8f1fefa))

* Almost There

Using ineritance to represent different versions
Most everything is done (for DowI, some errors may be present for DowII and DowIII)

Currently still rewriting relic-chunky cnonversions

Later some changes to serialization/deserialization for SGA might make some references non-circular

Also if it wasn&#39;t obvious, pretty much every test-case broke ([`05be19b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/05be19b8656263114b68893770cafea4d731a8ad))

* general commit

Going to start doing a rewrite, there&#39;s just too much bad rn ([`41c0a37`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/41c0a37ca35ddcf2964a8bf256c8e33050403d46))

* Massive Reorg

Not a full valid commit, who could have guessed that restructuring a complicated project would take a while and be wonky ([`fcc79cd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/fcc79cd51a15621aa4a265d90d603e9fbd7f2bda))

* Fix Ucs failing when line was not read ([`4db1321`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4db1321c3f5ebf8bd29d6d79850f89eeb7751e60))

* Tests now use archive_tools to unpack/pack stream

Also some general formatting

Also consider renaming structx.Struct to just StructX
On one hand it&#39;s nice to autograb Struct from either, BUT, it also feels kinda money-patchy

Better to use StructX anyways to make it obvious what&#39;s being used ([`ccca7bb`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ccca7bbd5c9d2bbe0b57c56f9a7ee47ba8c51589))

* RGT bashing

First step to extracting RGTs ([`eede178`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/eede1781ce320937db047c48f34ecb726bbaf86d))

* Disable dump_model &#39;dev_mode&#39;

Preferably I&#39;d do the smart thing and print out the stacktrace instead of raising the error (which closes the terminal)

But until i do that I&#39;ll keep hardcoding the sys-arg so I can test it in python

Alternatively, I could probably edit my IDEs runner so that the first arg is the path ([`67a4d8d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/67a4d8d3f6de3f1802162726be8a76a8734c4a3d))

* Merge branch &#39;testing&#39; into indev ([`64edf6a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/64edf6a919211cbeb5ce9481a2a3b04ad4ac46ed))

* Dow3 Model Support, Dumping Chunky Folder meta files ([`1d0553d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1d0553d8796005b5caea04d4ac8f735398b50d4b))

* Merge pull request #2 from ModernMAK/testing

Archive &amp; Chunky Tests ([`bceae22`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bceae22fb6734637a4d966f31070546a5ab3e431))

* Fix create/convert naming

Didn&#39;t I already do this? ([`d2b0e2b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d2b0e2bb99a0bc2f535f9b1d46312f0f82346fcd))

* Relic Chunky Tests ([`9464a7e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9464a7ef8c960e5ef57c6a2f79ab5b2cabcb1e41))

* Archive Test Support for Dow2/3

Assuming my test&#39;s aren&#39;t faulty, I can successfully unpack and repack most archives. ([`8949c47`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8949c47fb9c7805428bac7222071b5dd573fbeaa))

* Merge pull request #1 from ModernMAK/testing

Merge Testing into Main ([`0ba2c1b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/0ba2c1bac6dbdf96d7eb7ce2565dccb6120e242c))

* Update and rename main.yml to pytest.yml

Now runs on pushes to main and pr&#39;s to main; now I don&#39;t have to do wierd things like push to testing then to main

This also makes it so that testing can be used to add/remove tests instead of apply experimental features. ([`95e7861`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/95e78612fb9669892d771126fa38fd881e73cba4))

* Still trying to get pytest to work in actions

If I was doing this properly and just made a setup.py I wouldn&#39;t have to worry about this ([`0f9e735`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/0f9e735c778531beae9315aed2dbb8a54e4d1fea))

* Merge branch &#39;testing&#39; of https://github.com/ModernMAK/Relic-SGA-Archive-Tool into testing ([`bf47eee`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bf47eee64ff4e7ea88b51e7dcb39b5f4019d791c))

* Create conftest.py ([`462d80a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/462d80ad69c62c59308e567da263a351d350becc))

* Update main.yml ([`371de54`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/371de5461eeade5ba3dcd02e4b6880ed4d96bab3))

* Merge branch &#39;testing&#39; of https://github.com/ModernMAK/Relic-SGA-Archive-Tool into testing ([`9ef98ce`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9ef98cea6c7e69eea52f98898eb875469d95f38f))

* Create conftest.py ([`1d66a8b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1d66a8b1e3008b55c6c06f56a6bec867cc2db128))

* Update main.yml

Slash Fix? Ubuntu might be picky on slash type ([`ef7dca8`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ef7dca8452ef22368252e8e92ad69d8bd4d77c96))

* Hack to use both \src and \tests ([`ca11fe1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ca11fe1fca877f682cccb35330c7957ebfbf5ebc))

* Update main.yml ([`5f219a4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5f219a42f39eb7b02a91b4ec90c56e42dd8adc16))

* Create main.yml ([`f09e2cc`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f09e2ccdb687ccd44bbd258ef8f345dd064f2158))

* Bugfix getting root folder from tests\helper.py + writer for sample data ([`a75ed0f`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a75ed0fe06c90a6fddd6691a8642dc6e985e5f55))

* Ability To Repack an SGA (Poorly, but still) &amp; an SGA Test class

With this I can start testing SGA Unpacking into chunks without infringing on Relic&#39;s Copyright by distributing their SGA files, HOORAY.

This isn&#39;t perfect, and should NOT be expected to work for creating archives from scratch for the DoW games. ([`5afe267`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5afe2679cf2b83eacbc24311d6e00a7283839b82))

* Merge branch &#39;repacking-archive&#39; into testing ([`83fab9d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/83fab9d85c2c93202a9a0f548357fffdb49bb870))

* Fix dumper &#39;convert&#39;/&#39;create&#39; misnaming ([`3c402ab`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3c402ab5ea16fbf7ab8f365c6f03dc5ba802cf3a))

* Writer complete; time to test it ([`d0c0e9b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d0c0e9b546ccc383e397a48557d4b0377038058d))

* Repacking Archive

I really want to start having automated tests; but I also don&#39;t want to tread any further on the DoW IP. So by creating a system to repack Archives, I can build an archive in code, and unpack/repack to my hearts content. ([`d8ac8b9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d8ac8b9688a7ae258f4dce2e009c7c01be259911))

* Fix Version Bugs

Verion-Like Enums now use a base-class: VersionEnum, to allow for Version to impicitly compare values.

Version is now hashable (so it can be used in lookup)

Version now correctly performs equality (and no longer raises NotImplimentedErrors) ([`d8332e5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d8332e5181d967e0ba4f136104a73d014777ee58))

* MODEL Chunky + Tool work

Began work on &#39;Dump Model.py&#39; to dump Dow 1 &amp; 2 Models from a .whm or .model file (Dow 3 will follow suit after I figure out that format)

Added MODEL Chunky support (DOW 2). SKEL unsupported (admittedly, I don&#39;t want to bash my head against another heiarchal nightmare) and MESH partially supported. I assume Vertex count does change; but my code does not. Also; meshes which use shader&#39;s I haven&#39;t peeked at will not dump, I may change this in the future.

MODEL supports writing to OBJ/MTL file; via writer.py in Dow2\Model module

Chunk Collection now has helpers to simplify chunk conversion (get_data/folder_chunk/chunks)

MTL Writer now supports a bunch of 3rd party settings

In other news, my biggest regret is somehow letting PyCharm not auto-fix the chunk_formats when I moved them to Dow. I keep running into compilation errors because of it, and it makes debugging the &#39;tool&#39; that much harder.

In another strike against PyCharm; &#39;name&#39; may have been refactored into &#39;material_name&#39; where it should not have. ([`914ca43`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/914ca431b8fafe835c6604590d30672232d27fce))

* Made Version Reusable + Tool to dump Chunkies to Bin

dump_chunky is supposed to end up as a cmd-line pipable/drag-n-dropable tool currently, only supports Drag-n-Drop.

Version was moved to shared so that both SGA and Relic Chunkies could use it. Constants were moved to appropriate folders in each. An enum would be best but I couldn&#39;t decide on a suitable naming scheme (since I cant do 9.0 or 3.1). May consider using enum for SGA (since SgaVersion.Dow, SgaVersion.Dow2, SgaVersion.Dow3 makes sense) ([`531c506`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/531c506ce325cc0b923d1deae9dc8601096cd7ff))

* Bugfix for V9 unknown bytes &amp; import fixes ([`defde35`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/defde35645529022d426cddf2ea1dedd4a16bac7))

* Refactoring SGA

Keeping modules self-contained-ish

shared is now a catch-all for tiny classes which are used elsewhere

Headers are not seperated from their full versions (except for the archive_header, since that has several parts). Sparse Archive did get merged into the main archive file though. ([`4f0a64c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4f0a64ce6f2aed8a2d9bc87dd780ac172dec380a))

* DOW 3 Support

No Chunkies, but dumping the SGA works ([`9f1ef6c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9f1ef6c9dad524a64f2570a65a20f39ac67c4459))

* Merge branch &#39;indev&#39; into DOW-2 ([`c90dbb5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c90dbb5f9237c4cedafcbc633b26a057283c2a76))

* Description =&gt; Virtual Drive

Renaming ([`5994949`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5994949780d8d2a3b3c1f81130b48ecb4618fde7))

* Support for DOW2 Archives (SGAv5) ([`99131e7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/99131e78ae03559905346bb6d06dfda73e654563))

* Attempt @ Euler Angles ([`3165851`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/31658517d0aab18cad96628e3b35b3f21a7e48a6))

* V3 Failure

Day 3 of Insanity; The numbers speak to me...
Joke&#39;s aside; bashing my head against this just isn&#39;t working.

I&#39;t partially works: most bones look right.

Some bones just don&#39;t and I can&#39;t tell if it&#39;s my data parsing, coordinate system mismatch, misapplying matrix calculations; what have you. ([`e8fe1fa`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e8fe1fa72f3e3533b950dcd0399f8f0df2e22e9f))

* Layout has been validated (cooraoborated may be better term)

A script to import WHM into 3dsMax confirms my thoughts that the layout is pos(XYZ ), quaternion(XYZW).

But the script also shows that it uses local transforms?

Skeleton was fairly close to being correct; and this avenue was a complete bust (unless I missed something)

I&#39;ll take the win of confirming my thoughts on the layout ([`75b29ea`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/75b29ea164e5fdfb048a3ca313169987f0fb1515))

* QOL made whm a module (to avoid imports from individual files) ([`e2b7a75`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e2b7a7507dff483d217b3a17974b946ccaff92ce))

* Reorg ([`850e0c9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/850e0c9cc85be53ed46a0ecafbfe4573feca20c9))

* QOL condensing modules ([`8ec9450`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8ec9450588c107d84d7869bc9bb3b6f9d0e7aa4b))

* Some work on SKEL

SKEL blocks contain 7 floats

I believe it&#39;s a Float3 Position and a Float4 XYZW Quaternion

The positions appear to be relative to the prevoius bone ([`8e6e59d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8e6e59d5b432aefb8b2164b3a083d960ed292b47))

* WHM fully implimented

WHM should be able to be completely unpacked into it&#39;s specific chunk layouts.

Some work on deciphering SKEL may  be included in this commit. This is not intentional. ([`d2ea260`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d2ea260b7d13c7d6fc85ef49fac4340cc4c01eb5))

* Update Scan Compression Flag.py ([`12dd580`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/12dd58019682c8362864f1b32d3e6dddce107ca9))

* Writer Code Cleanup

Github Desktop Split Beta Bug? These changes were selected in the last commit but didn&#39;t go through? ([`f782f31`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f782f31e79e61a9a8d2da35a9f3fdc4805c119f7))

* Normals Work

So blender 2.9 correctly uses Face Windings and 2.8 does not is the takeaway I got from this.
Blender 2.9 was correctly showing me lighting, but because the face-winding was wrong, I assumed it was wrong too; since 2.8 looked fine. ([`010b25e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/010b25efce95bb9e73606e34ec016d9dc8de911a))

* Formatting ([`53c71df`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/53c71dfd4c39d23783325338e061e28ffee12994))

* Fix normals not being flipped for flipped model. Changed directory helpers in config

Config now has filter_ and get_ to make it easier to get the latest installation. ([`9b83c39`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9b83c390eecef830130a395c02b593613e5ba889))

* Fix WHM dumping

This flips the X axis; which should correct text being incorrectly displayed in the material.
We also manually specify the extension for our temp file&#39;s input; since TexConv will throw an error if it reads a TGA without an extension ([`cf06629`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/cf06629c05ba89a7a159ab1e169727eecce58da7))

* Added option to force MTL filename&#39;s to be valid. Fixed TexConv not using converted file.

I forgot TexConv auto-adds the extension of the new file; great for everycase except this one. So I need to get the new_ext file somehow. I could do a scan and find the file with an ext. but I just hack it to a lookup table.

MTL&#39;s texture paths cannot contain spaces; which sucks. (They don&#39;t follow the double-quotes rule; I already checked). So if you want it to autograb your textures, you need to force them to be valid first. ([`38ccfd0`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/38ccfd03e29b7902434525016f55f85924262d46))

* Somehow broke OBJ writer again

Lovely; time to examine commits ([`c9a09c4`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c9a09c434c4f20aeb28088fc93098a8fe4903958))

* Fixed Dumper include_meta

Previously was using file_path (which has been dropped) instead of output_path ([`e61e41c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/e61e41ca06c963fcf35ebfcaf1f1d64fe0b5b84d))

* Update relic_chunky_header.py

type_br now correctly uses &#39;\x1a (26 ~ &#39;Sub&#39;)&#39;

Apparently, some OSs use this as a line break; so type_br is a &#39;catch-all&#39; linebreak? ([`ca22812`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ca22812a703f2b57561755751d4d31e8c82c7c35))

* WTP uses ImagConverter &amp; error handling for empty name in localisation search ([`1eea6c9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1eea6c9428bb4839420b09cfb2586cf01c0d2c48))

* Fixed case where &#39;b&#39; invalidates a localisation string

see src\relic\ucs.py ([`a5222b1`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a5222b1da318c0155a4995aa07ff5ce3134f646a))

* Universal Dumper

+ A lot of changes to make it work, mainly changes with error handling ([`bbb66c3`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/bbb66c3ed62d68950658a6c9b65538efe64281f0))

* Config now properly uses WinReg to get steam dir

Added a helper function to get unique DOW game directories
Added a helper function to get the latest DOW game directory
Added an enum to classify the game without scanning the path
Fixed the dll_path in config (was not reaching src directory) ([`6628c9b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/6628c9bebe2af096548134c5e040510d12815a7e))

* Dumping, Config, Converters

Master dumper file for chunks in chunk_formats

FdaConverter has more use cases

RSH dumper now has a converter to write Imag files better

WHM chunky failures now use UnimplimentesMslcBlockFormat, which inherits NotImplimentedError for compatability. Allows specifically catching this error (as opposed to the generic valueerror/keyerror/unimplimentederror handlers

WHM writer has more generalized use case

Chunk colection walk now acts similiarly to os.walk

First steps to using config ([`8bd1534`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8bd15345aa6698bd3a53cc53b83c9636c2fede6b))

* Folder uses file path name; walk should now correctly express paths ([`b2d4e37`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/b2d4e378fe4293713a26d5d216b5ba956fede61c))

* Forgot to actually fix the heiarchy in Archive

Also some fixes that I forgot to commit ([`381fc5b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/381fc5b31f6f1066072960d454021731a5955278))

* Fixed archive not using Abstract Directory + SGA Dumper ([`38d06bc`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/38d06bc0517f6bfbcfb5b01256ae7f3f1f6b35dc))

* Archive Walking &amp; starting files for unsupported formats ([`db03457`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/db034578f5759acb2a61bed327425750722fabb6))

* Walk improvements + Script to scan all sga&#39;s for nested unsuported chunky files ([`a333ea7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a333ea7486edc4104a7868e20416a56fd84a9f63))

* Formatting and walk changes ([`3275019`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/32750198d415b475b20edae17d0ab12ee8528ea2))

* Create archive.sga

Sample archive.sga (not filled in yet)

Need to generate a blank SGA ([`7a1e57a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7a1e57a70ee3a0e69a6defda534f43e3049e42c0))

* init tests ([`15c8c90`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/15c8c901ca5c40a9322660529bb5930f9bc641f6))

* Repack methods ([`a5fbf76`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a5fbf76cfbc0dd40a6d3a45496addff3f861de38))

* Refactored archive, dropped &#39;flat&#39; classes ([`56f69a5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/56f69a507406263b5349ac7314e126d83fe75acf))

* Lots of refactoring

Next up; do what I did to RelicChunky to SGA ([`dda13ed`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dda13edcb4ef6476370bc7edf2c222f0f5102d19))

* Relic Chunky now can check for the Magic Word indipendently, and a walk function has been added to filter walk results ([`8aed6ad`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8aed6add173a3178548fdd4e3aa31118447a55e3))

* organizing ([`723c04c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/723c04c734f8ccc51cadda05291ba1f9b78b6ebe))

* Merge branch &#39;main&#39; of https://github.com/ModernMAK/Dawn-Of-War-I into main ([`c9747f2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c9747f21ebf93423785db71febdee8844ff56f1e))

* Merge branch &#39;main&#39; of https://github.com/ModernMAK/Dawn-Of-War-I into main ([`1729f25`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/1729f25a425b12112e72433ac93424b039f086dd))

* UCS parser

This isn&#39;t in an archive, and is a super stupid simple file; which is exactly why I cranked out a script to extract it ([`dc948fa`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dc948fa5e47ab3416a0994b442f36bd874f3714d))

* Merge branch &#39;main&#39; of https://github.com/ModernMAK/Dawn-Of-War-I into main ([`be7087b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/be7087b031a4f7392424cc8841d70e6b5799bcc0))

* Added assertions to Mesh_IO

Specifically to float reads, NAN for a position, normal, or UV is a sign of a bad parsing.

This will also work with my -funky relocator so wierd WHMs getm oved to the funky folder ([`cacfa98`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/cacfa98ac4df3ac55f3987a7e8c4856f2e7dc0f4))

* Update requirements.txt ([`f8cb16d`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f8cb16d5d65cc810c6312ec9db561332160643d9))

* Create Blender Obj2Fbx.py

Blender script to convert  obj to fbx ([`8b5b107`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8b5b107f848da1e821b2c6de0285f7a59002de0f))

* Fixed illum mode + Basic Transparency in Blender

Since Unity pulls an OBJ as a big file instead of submeshes, I wanted it working in blender, so I can import, convert, then export it again.

In the future, when I crack SKEL, I will not use OBJ anyways, and this will be a moot point aside from an alternative model format. ([`7334941`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7334941a37124bc2b58e33ec625034c8caed9617))

* WHM materials work

I&#39;d prefer to not copy textures over into the WHM dump directory, so I specify the RHS directory instead.

I know understand why obj files use 1/1/1 2/2/2 3/3/3 etc
Frankly, I&#39;m surprised it doesn&#39;t assume  vn and vt use the same index, but i bet it&#39;s because the specification doesn&#39;t OR its a parser thing. ([`cb06681`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/cb066815d09d02c14ffaffc48575a0f6a8aec0b7))

* Divvying up WHM to make it easier to look through ([`36017a9`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/36017a99fc109a4a12d8886f1d5d7edd3332f62b))

* Added a MTL writer

Currently we don&#39;t create a mtl to match the obj file created. With this, we can. ([`9e2a700`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9e2a700257e8d4ffde24b6ca64b1c5417efcbb1e))

* Update config.py ([`f1f3883`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f1f3883c2e30147b5eb47b77051cfa15667f5c6c))

* relic.chunky now exposes most common classes in a single module (the relic.chunky module) ([`495fc71`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/495fc7106dd1d979099591e5fa9148e55cd3e8c6))

* Fixing up TeamTex Dump

A lot of TLC to make it reusable.

SGA&#39;s also got cleaned

Added a config py file, was planning on using it to manage dump paths, but I&#39;ll probably use it as a way of automatically fetching the steam directories to dump. ([`8122382`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8122382ed7d1410940530e482a6b7d4978ed5a27))

* Dropped  aifc2fda &amp; fda2aifc

Probably shouldn&#39;t have included those in the first place, non-vital and my dumps didn&#39;t work properly (or I wasn&#39;t using it right). ([`a535672`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a5356721afed5c3f6de5a371f1f0bb172ef05a3b))

* Doing some cleanup ([`d14d0a7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/d14d0a71401cc36a6d6250c547459edd185ff893))

* Fixed .layer =&gt; .unk_a

Could have sworn I fixed this already. Did it get reverted? ([`9396a7b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/9396a7b03d601a27b2d2a8042cf99425cc0befa0))

* WHM cleanup done ~ dump working for most meshes

I haven&#39;t checked materials working, but importing the full models correctly

Later, when I try to dump skeleton data, I&#39;ll like stop supporting OBJ (since it can&#39;t handle skeletons), but with any luck, the obj exporeter will still work. ([`2327ccd`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2327ccd7f58956f0005a645abff755b065f8a5ee))

* Spltting OBJ file stuff from whm &amp; stripping whm comments for now

whm is kinda bulky with all my attempts, some TLC will help me read it better ([`7366f91`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7366f9178b8b4647715f81a29cbfed7f2920ff29))

* Fixed dump_model when full=True

I had to import each part in blender first to validated that I&#39;d correctly dumped them.

After doing that, (and setting v_offset to 0 for a full dump, i&#39;d realized I was doing v_offset += v_offset+v_count (count of vertex in part) instead of v_offset += v_count or v_offset = v_offset+v_count ([`08c61b6`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/08c61b6e725f244059ccf3862a60e4f4bce7752a))

* whm still a mystery ([`3d4db4e`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3d4db4eeb22886212ce48cb85c43361f9a3a7778))

* Merge branch &#39;chunky-cleanup&#39; into temp ([`984054a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/984054a34e1936665961b524a291a0653bd56c68))

* Moved whm ([`62cff3a`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/62cff3a6f3e2d3339d8bda15e5d983a3814d230b))

* Confirmed Speed Up

22 vs 415+ seconds, (most of that time was due to file open/writes/closes, but still) ([`2801ef5`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/2801ef50e7bd7bc0a67159712a1df8ce068e98f3))

* Fix walks in chunk_collection

Due to an indent error; alot of extra cycles were being done, which likely caused the slowdowns I was seeing ([`63a7025`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/63a7025691112c16e9174e5cd1da32cc93f0070c))

* Chunky moved to seperate files

I dislike big modules, probably due to my C# background; unlike my EG2 mess, chunky only needed Data &amp; Folder formats, so I could use a locally imported &#39;reader&#39; file to store the logic shared between them. ([`3f90650`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3f90650fbf513840573893e8e9700efb4694da9d))

* Still haven&#39;t cracked the WHM format ([`be9b1d6`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/be9b1d6f2e69bed2c4eab50b71390c48a0dbe3fa))

* Update whm.py ([`963b776`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/963b7766b0a7ae83c5a3747ec2362b05513087ec))

* Fixes errors from refactoring

Makes ChunkType an enum,
FDA uses proper get_chunk method
DGA&#39;s reverted unk_a refactoring into layer (due to both InfoChunks being named the same?) ([`a72e84c`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a72e84cc11d50c665686974a2536979d6809fc8c))

* Revert &#34;Model Prototyping&#34;

This reverts commit 8dcfdf72009b7c2b293fbc06ac0d47bc5cc691e4. ([`7250d64`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/7250d64eda2a762e112a51a69e576e5b2f27abb0))

* Model Prototyping

Still don&#39;t know the model file&#39;s layout.
What I do know:
Layout doesn&#39;t include padding to 16 byte boundaries (positions are 12 bytes)
Buffer is not interleaved (pos, normal, and uv are all grouped)
Most meshes are 32 or 48 bytes, others are weird like 87.5 bytes

32 vertex size  is Position:Float3, Normal:Float3, Uv:Float2
48 vertex size  is Position:Float3, Unknown:Float4, Normal:Float3, Uv:Float2
87.5... no idea ([`8dcfdf7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8dcfdf72009b7c2b293fbc06ac0d47bc5cc691e4))

* wtp improvements ([`dc715db`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/dc715db6be9a6ddaae7d9adc0a31bfeb8e3bdf83))

* DDS Fix via DirectXTex (texconv)

A simple subprocess cmd which safely flips images vertically; my previous implimentation using PIL didn&#39;t work (perfectly), I imagine due to the limited support PIL has for dds. ([`8574e01`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8574e01ee8e0249636a86345a2abe1fba99cd5c8))

* mslc_chunk &#39;unk_b&#39; possible buffer format &amp; WTP support

While dumping all obj files I found that some files failed (due to running out of data to read) so I checked the vertex buffer and sur enough, the size per vertex was different (calculated by dividing the buffer via the vertex count)

The only noticible change between the two being unk_b (other fields changed but too inconsistant to be meaningful)

While I haven&#39;t proven it yet, this change fixed most issues (still some ascii decode issues? and some unpacking issues, hopefully unrelated) ([`8e5889b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/8e5889bbeb593fb023764c84f90386807d85309f))

* Texture ripper works

On all files I have from soulstorm anyways

IMAGES.py simply copies all raw images from A to B
rsh.py handles textures in rsh archives

Since these are not the teamable textures, I may need to reinvent the wheel on this ([`30ca0fa`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/30ca0fa51d85734f6af363bcd235dd1c705d4b25))

* chunk dumps for mats/animations

Also some more knowledge on meshes. SKEL and Materials are my next targets. ([`a508637`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/a5086376574358e718e7dee7353827f8f89c9f8c))

* Basic Mesh Export (Pos / Tris only), submeshes not merged

I still need to make submeshes children of parent meshes &amp; figure out how to do .mtl ([`ddce209`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/ddce2098849bf0300a251b58e117c0335880dd71))

* more mesh stuff ([`5ec9238`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5ec9238e436a5ff507e0bf00ad9a3db46f916c5d))

* stupid simple images (Via Pillow)

Since DOW has both dds and tga&#39;s side by side, I preserve the format extension in the dumped filename so I can choose the better file ([`5d359df`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/5d359dfc1f37ba0837c845d4439c39b10213c870))

* FDA &#39;fixed&#39;

Literally, using a &#39;fixed&#39; sample _rate value seems to make audio files come out properly. ([`4118edc`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/4118edcb360fb6d9de647fc32d5755dd0e381f36))

* Something is wrong; fda2aifc-dec works perfectly mine (aiffr-dec) is lower quality and cuts off ([`c3820ef`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/c3820ef6814f92aad93c9eb170c2d93416fbe1a9))

*  minor change to subprocess calls

dec seems to dislike long path names (bet the buffer is only 256 or something, since that used  to be the max)

fda2aifc doesn&#39;t seem to read my fda&#39;s properly, dont know why... Good thing I decided to build my own writer ([`3ea524b`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/3ea524b89e52b140d2d01892c77017aed2f4fcc5))

* Manually construct AIFF-C (Relic) files

Works, although ieee754 (80bit) floats probably dont work as intended ([`735a143`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/735a1439752ff1c2f1916cd431572bfc0d89a55d))

* Unpacking successful ([`f241be2`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/f241be2ed7f717c647004343561c03a33c2880ac))

* Init Commit ([`60131de`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/60131de74bbb7d9cb553d139206beab655dcf6ba))

* Initial commit ([`783c2f7`](https://github.com/MAK-Relic-Tool/Relic-Tool-Core/commit/783c2f791ee23c22fe2384567963f682f0024555))
