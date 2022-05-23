#!/usr/bin/env bash

RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
BOLD=$(tput bold)
RESET=$(tput sgr0)
PATTERN="^(([0-9]+)\.([0-9]+)\.([0-9]+))(-(alpha|beta|rc)([0-9]+))?$"

usage() {
	cat <<- EOF

	USAGE:
	==================================
	 $0 [options] release-type [release-message] [-f <releasenotes.md>]

	 RELEASE-TYPE:
	 ------------
	 Release a new version. when the current release is a staged version (alpha, beta, rc)
	 The stage type should be used to release a next staged version.

	 major: release version (X+1).0.0
	 minor: release version X.(Y+1).0
	 patch: release version X.Y.(Z+1)
	 stage: release the next version of a stage or the next staged version
	        the order is alphaX -> betaX -> rcX -> final
	        When a major, minor or patch release is done, you will be asked if you wan to
	        release a staged version, or the final version.

	 RELEASE-MESSAGE:
	 ----------------

	 The name of the release. This will be passed when creating the tag as the message of the tag

	   git tag -m "release-message'

	 When the release is created during deployment, this is also used as the title of the release.
	 When not set, during the bumping you are asked to provide it.

	OPTIONS:
	---------
	  -h, --help                   show this menu
	  -y, --non-interactive        Run in non interactive mode.
	                               Only allowed on major, minor and patches.
	                               Requires <release-message> to be passed.
	  -f, --file <releasenotes.md> Use a file for the release-note. Can be used in
	                               combination with non-interactive mode.
	                               Text file should be a plain text file like markdown
	  -v, --version                show the current version of the library
	  bump version to a new major, minor or patch
	  first argument should be major, minor or patch
	  this script update package.json version
	  commits package json and create tag
	  Can only be run on main.

	  If you want to release an alpha of a new version,
	  use major minor or patch.
	  You will be challenged to choose the stage version

	  i.e current version is: 2.4.4 and you want to release a minor alpha (2.5.0-alpha1)
	  use the minor argument: '$0 minor'

	  If you want to release the next stage, i.e 2.3.3-alpha1 -> 2.3.3-alpha2,
	  use the stage argument: '$0 stage'

	  if you want to move to the next stage, i.e 2.5.6-beta3 -> 2.5.6-rc1, use the stage argument: '$0 stage'

	  version match pattern: '$PATTERN'

	EXAMPLES:
	---------
	  $0 major : update version 0.1.2 -> 1.0.0
	  $0 minor : update version 0.1.2 -> 0.2.0
	  $0 patch : update version 0.1.2-rc4 -> 0.1.3
	  $0 stage : update version 1.1.1-beta1 -> 1.1.1-beta2

	  $0 minor 'My awesome release' -f RELEASENOTES.md -y

	EOF
}

show_version () {
    G_CURRENT_RELEASE_VERSION=$(jq -r '.version' package.json)
    # TODO: strip newlines
    G_CURRENT_RELEASE_NAME="$(git tag -l "v$G_CURRENT_RELEASE_VERSION" --format "%(contents:subject)")"
	cat <<- VERSION

	The current version of the library ($(jq -r '.name' package.json)):

	  Version: $G_CURRENT_RELEASE_VERSION
	  Name:    ${G_CURRENT_RELEASE_NAME:-No release name available}
	  Tag:     v$G_CURRENT_RELEASE_VERSION

	VERSION
}

error () {
  >&2 echo "${RED}${BOLD}[ERROR] $* ${RESET}"
  echo ""
}
warn () {
  >&2 echo "${YELLOW}${BOLD}[WARN]${RESET} $*"
  echo ""
}

info () {
  echo "${BLUE}${BOLD}[INFO]${RESET} $*"
  echo ""
}

INTERACTIVE="true"

ARGUMENTS=( )
for ARG in "$@"; do
    case "$ARG" in
        --version|-v)
            show_version
            exit 0
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        --non-interactive|-y)
             INTERACTIVE="false"
             ;;
        --file|-f)
            if [[ ! -f "$2" ]]; then
                error "'$2' is not a valid file"
                exit 1
            fi
            RELEASE_NOTES_FILE="$2"
            shift
            ;;
        *)
            ARGUMENTS+=( "$ARG" )
            ;;
    esac
    shift
done

RELEASE_TYPE="${ARGUMENTS[0]}"
RELEASE_NAME="${ARGUMENTS[1]}"

if ! [[ "$RELEASE_TYPE" =~ ^(major|minor|patch|stage)$ ]]
then
    error "Use major, minor, patch or stage"
    usage
    exit 1
fi

# Check that for non-interactive releases the release name is provided
if [[ "$INTERACTIVE" == "false" ]] && [[ -z "$RELEASE_NAME" ]]; then
    error "For non-interactive releases, the release-name is required"
    exit 1
fi

if [[ "$(git rev-parse --abbrev-ref @)" != "main" ]]; then
    if [[ "$INTERACTIVE" == "false" ]]; then
        error "staged releases are only allowd from main branch"
        exit 1
    fi

    warn "You are trying to release from a branch other than 'main'"
    read -p "Are you sure you want to continue? [y/N] " RELEASE_NOT_MAIN
    if ! [[ "$RELEASE_NOT_MAIN" =~ ^[yY] ]]; then
        exit 2
    fi
fi

git fetch origin
UP_TO_DATE=$(git status -uno | grep "Your branch is behind ")
echo $UP_TO_DATE
if ! [[ -z "${UP_TO_DATE}" ]]; then
    cat <<- STATUS
	Branch is behind remote.
	You might want to pull first?
	If you continue now, the tag will not be on the head.
	Do you want to continue?

	c: Continue anyway, q: quit, p: pull and continue?
	STATUS

    read -p "[Q/p/c]? " CONTINUE

    echo $CONTINUE

    if [[ "$CONTINUE" =~ ^[pP] ]]; then
        git pull
    elif [[ "$CONTINUE" =~ ^[cC] ]]; then
        read -p "Continuing without pulling. Are you sure? Press Ctrl+C to cancel" SURE
        break
    else
        echo "break"
        exit 1
    fi
fi

# pick version value from package.json
CURRENT_VERSION="$(jq -r .version package.json)"
IS_STAGED_BUILD="false"


if [[ "$CURRENT_VERSION" =~ $PATTERN ]]; then
    FULL_VERSION=${BASH_REMATCH[0]}
    VERSION_NUMBER=${BASH_REMATCH[1]}
    MAJOR=${BASH_REMATCH[2]}
    MINOR=${BASH_REMATCH[3]}
    PATCH=${BASH_REMATCH[4]}
    STAGE=${BASH_REMATCH[6]}
    STAGE_NUMBER=${BASH_REMATCH[7]}
fi

if ! [[ -z "$STAGE" ]]; then
    IS_STAGED_BUILD="true"
fi

next_stages () {
    local n="$2"
    local c="$1"

    if [[ -z "$c" ]]; then
        echo "[a]lpha$((n + 1))" "[b]eta1" "[r]c1" "[f]inal"
    elif [[ "$c" == "alpha" ]]; then
        echo "[a]lpha$((n + 1))" "[b]eta1" "[r]c1"
    elif [[ "$c" == "beta" ]]; then
        echo "[b]eta$((n + 1))" "[r]c1"
    elif [[ "$c" == "rc" ]]; then
        echo "[r]c$(($n + 1))"
    else
        error "Can't determine next stages"
        error "$c"
        exit 2
    fi
}

next_stage () {
    local n="$1"
    local c="$2"

    if [[ "$c" == "final" ]]; then
        echo "final"
    elif [[ "$c" =~ ^(alpha|beta|rc)([0-9]+)?$ ]]; then
        if [[ "${BASH_REMATCH[1]}" == "$n" ]]; then
            echo "$n$((${BASH_REMATCH[2]} + 1))"
        else
            echo "${n}1"
        fi
    else
        error "Invalid parameters"
        exit 2
    fi
}

allowed_stages () {
    local c="$1"

    if [[ -z "$c" ]]; then
        echo  "^[aAbBrRfF]"
    elif [[ "$c" == "alpha" ]]; then
        echo  "^[aAbBrR]"
    elif [[ "$c" == "beta" ]]; then
        echo  "^[bBrR]"
    elif [[ "$c" == "rc" ]]; then
        echo  "^[rR]"
    fi
}

select_stage_type () {
    local current_stage="$1";
    local curent_stage_number="${2}"
    local -a stages=( $(next_stages $current_stage $curent_stage_number) )

    >&2 echo "What stage do you want to release?"
    read -p "$(echo ${stages[@]}): " NEXT_STAGE

    if ! [[ "$NEXT_STAGE" =~ $(allowed_stages $current_stage $curent_stage_number) ]]; then
        error "Invalid input"
        exit 2
    fi

    if [[ "$NEXT_STAGE" =~ ^[fF] ]]; then
        echo "final"
    elif [[ "$NEXT_STAGE" =~ ^[aA] ]]; then
        echo "alpha"
    elif [[ "$NEXT_STAGE" =~ ^[bB] ]]; then
        echo "beta"
    elif [[ "$NEXT_STAGE" =~ ^[rR] ]]; then
        echo "rc"
    else
        error "Invalid stage"
        exit 2
    fi
}

## For Major, minor and patches, release current version without stage
# when current build is staged build
if [[ "$RELEASE_TYPE" =~ ^(major|minor|patch)$ ]] && [[ "$IS_STAGED_BUILD" == "true" ]]; then
    if [[ "$RELEASE_TYPE" == "major" ]]; then
        if [[ "$MINOR" == "0" ]] && [[ "$PATCH" == "0" ]]; then
            NEXT_VERSION="$((MAJOR)).0.0"
        else
            NEXT_VERSION="$((MAJOR + 1)).0.0"
        fi
    elif [[ "$RELEASE_TYPE" == "minor" ]]; then
        if [[ "$PATCH" == "0" ]]; then
            NEXT_VERSION="$((MAJOR)).$((MINOR)).0"
        else
            NEXT_VERSION="$((MAJOR)).$((MINOR + 1)).0"
        fi
    else
        NEXT_VERSION="$((MAJOR)).$((MINOR)).$((PATCH))"
    fi
elif [[ "$RELEASE_TYPE" = "major" ]]; then
    NEXT_VERSION="$((MAJOR + 1)).0.0"
    if [[ "$INTERACTIVE" == "true" ]]; then
        NEXT_STAGE_TYPE=$(select_stage_type)
        if [[ "$NEXT_STAGE_TYPE" != "final" ]]; then
            NEXT_VERSION="${NEXT_VERSION}-${NEXT_STAGE_TYPE}1"
        fi
    fi
elif [[ "$RELEASE_TYPE" = "minor" ]]; then
    NEXT_VERSION="$((MAJOR)).$((MINOR + 1)).0"
    if [[ "$INTERACTIVE" == "true" ]]; then
        NEXT_STAGE_TYPE=$(select_stage_type)
        if [[ "$NEXT_STAGE_TYPE" != "final" ]]; then
            NEXT_VERSION="${NEXT_VERSION}-${NEXT_STAGE_TYPE}1"
        fi
    fi
elif [[ "$RELEASE_TYPE" = "patch" ]]; then
    NEXT_VERSION="$((MAJOR)).$((MINOR)).$((PATCH + 1))"
    if [[ "$INTERACTIVE" == "true" ]]; then
        NEXT_STAGE_TYPE=$(select_stage_type)
        if [[ "$NEXT_STAGE_TYPE" != "final" ]]; then
            NEXT_VERSION="${NEXT_VERSION}-${NEXT_STAGE_TYPE}1"
        fi
    fi
elif [[ "$RELEASE_TYPE" = "stage" ]]; then
    if [[ "$INTERACTIVE" == "false" ]]; then
        error "staged builds are not supported in non-interactive mode"
        exit 1
    fi

    if [[ "$INTERACTIVE" == "false" ]]; then
        error "staged releases are only allowed in interactive mode"
        exit 1
    fi
    # check if current version is staged
    if [[ "$IS_STAGED_BUILD" == "false" ]]; then
        error "The current version is already final. Use major, minor or patch to release next staged version"
        exit 2
    fi
    CURRENT_STAGE="${STAGE}${STAGE_NUMBER}"
    NEXT_STAGE_TYPE=$(select_stage_type $STAGE $STAGE_NUMBER)
    NEXT_STAGE=$(next_stage $NEXT_STAGE_TYPE $CURRENT_STAGE)
    NEXT_VERSION="$((MAJOR)).$((MINOR)).$((PATCH))-$NEXT_STAGE"
fi

if ! [[ "$NEXT_VERSION" =~ $PATTERN ]]; then
    error "Invalid version $NEXT_VERSION"
    exit 2
fi
info "Continue to release '$NEXT_VERSION'"
# update package.json

INSTALL_DIR="/tmp/$(jq -r '.name' package.json)/$NEXT_VERSION"
if [[ -d "$INSTALL_DIR" ]]; then
    # FORCE wipe for non-interactive releases
    if [[ "$INTERACTIVE" == "true" ]]; then
        echo "Directory '$INSTALL_DIR' is not empty"
        echo " [y]: wipe directory and continue"
        echo " [n]: Quit (manually wipe first)"
        read -p "Wipe directory first? [y/N] " WIPE_FIRST
    else
        WIPE_FIRST=y
    fi

    if [[ "$WIPE_FIRST" =~ ^[yY] ]]; then
        rm -rf "$INSTALL_DIR"
    else
        exit 1
    fi
fi


CURR=$(pwd)
cleanup () {
    cd $CURR
    rm -rf $INSTALL_DIR
}

mkdir -p $INSTALL_DIR
PACKAGE_JSON=$INSTALL_DIR/package.json
PACKAGE_LOCK_JSON=$INSTALL_DIR/package-lock.json
jq -r --arg nv "$NEXT_VERSION" '.version |= $nv' package.json > $PACKAGE_JSON
jq -r --arg nv "$NEXT_VERSION" '.version |= $nv' package-lock.json > $PACKAGE_LOCK_JSON

## Use trap to clean up the environment on exit, quit or error
trap cleanup ERR SIGINT EXIT
## Change dir and run npm install to fix the files
pushd $INSTALL_DIR
info "Using npm install to apply updated version"
npm install --omit=dev
popd

mv $PACKAGE_JSON package.json
mv $PACKAGE_LOCK_JSON package-lock.json

cat <<- CHANGES
Please review the diff
-----8<-----------8<------
CHANGES
git --no-pager diff --minimal -- package{,-lock}.json
echo "-----8<-----------8<------"

if [[ "$INTERACTIVE" == "true" ]]; then
    read -p "Do the changes look good? [Y/n] " APPLY_CHANGES
else
    APPLY_CHANGES=y
fi

if [[ "$APPLY_CHANGES" =~ ^[nN] ]]; then
    git checkout -- package{,-lock}.json
    exit 1
fi

# add optional commit message extend
if [[ -z "$RELEASE_NAME" ]]; then
	cat <<- RELEASE

	    Give the release a descriptive name:

	RELEASE
    read RELEASE_NAME
fi

if [[ ! -e "$RELEASE_NOTES_FILE" ]] && [[ "$INTERACTIVE" == "true" ]]; then
    read -p "Add release notes? (use <Enter> <Ctrl-D> to continue when done) [Y/n] " RN
    if [[ $RN =~ ^[yY] ]] || [[ -z "$RN" ]]; then
        echo ""
        echo "-----------8<-------8<---------------"
        __=""
        _stdin=""

        read -N1 -t1 __  && {
            (( $? <= 128 ))  && {
                IFS= read -rd '' _stdin
                _stdin="$__$_stdin"
            }
        }
        _stdin="$(awk '{print}; END {print "|||"}' /dev/stdin)"
        RELEASE_NOTES="${_stdin%|||}"
        echo "-----------8<-------8<---------------"
        echo ""
        sleep 1
    fi
elif [[ -e "$RELEASE_NOTES_FILE" ]]; then
    RELEASE_NOTES="$(cat "$RELEASE_NOTES_FILE")"
fi

cat <<- APPVERSION > wsgi_app/appversion.json
{
    "version": "v${NEXT_VERSION}",
    "sha": "$(git rev-parse HEAD)",
    "description": "$(echo $RELEASE_NOTES | awk -v ORS='\\r\\n' '1')"
}
APPVERSION

git add package{,-lock}.json wsgi_app/appversion.json
git commit -m "[RELEASE] bump version: $CURRENT_VERSION -> $NEXT_VERSION $EXTRA_MESSAGE

$RELEASE_NAME"
git tag v$NEXT_VERSION -m "$RELEASE_NAME" -m "$RELEASE_NOTES"

if [[ "$INTERACTIVE" != "true" ]]; then
    exit 0
fi
echo "Run 'git push' and 'git push --tags' to get the release deployed"

read -p "Want to push the release right now? [y/N] " PUSH_RELEASE

if [[ "$PUSH_RELEASE" =~ ^[yY] ]]; then
    git push
    git push --tags
fi

